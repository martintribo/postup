#!/usr/bin/env python3
"""PostUp R2 spend kill switch: disable r2.dev when Class B reads exceed thresholds.

Secrets come from ~/.config/postup/cloudflare.env (never git).
Re-enable is manual: `killswitch.py enable`.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

CLASS_B = {
    "HeadBucket",
    "HeadObject",
    "GetObject",
    "UsageSummary",
    "GetBucketEncryption",
    "GetBucketLocation",
    "GetBucketCors",
    "GetBucketLifecycleConfiguration",
}

GQL_URL = "https://api.cloudflare.com/client/v4/graphql"
CF_API = "https://api.cloudflare.com/client/v4"

GQL_OPS = """
query R2Ops($accountTag: string!, $start: Time, $end: Time, $bucketName: string) {
  viewer {
    accounts(filter: { accountTag: $accountTag }) {
      r2OperationsAdaptiveGroups(
        limit: 10000
        filter: {
          datetime_geq: $start
          datetime_leq: $end
          bucketName: $bucketName
        }
      ) {
        sum { requests }
        dimensions { actionType datetimeHour }
      }
    }
  }
}
"""


class AnalyticsUnauthorized(RuntimeError):
    pass


class ConfigError(RuntimeError):
    pass


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"{ts} {msg}", flush=True)


def load_env_file(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def cfg() -> dict[str, Any]:
    load_env_file(Path.home() / ".config/postup/cloudflare.env")
    load_env_file(Path.home() / ".config/postup/killswitch.env")
    token = os.environ.get("CLOUDFLARE_API_TOKEN") or ""
    account = os.environ.get("CLOUDFLARE_ACCOUNT_ID") or ""
    if not token or not account:
        raise ConfigError(
            "CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID required "
            "(~/.config/postup/cloudflare.env)"
        )
    state_dir = Path(
        os.environ.get("KILLSWITCH_STATE_DIR")
        or (Path.home() / ".config/postup/killswitch")
    )
    return {
        "token": token,
        "account": account,
        "bucket": os.environ.get("R2_BUCKET", "postup-tiles"),
        "mtd_threshold": int(os.environ.get("KILLSWITCH_MTD_CLASS_B", "50000000")),
        "burst_threshold": int(
            os.environ.get("KILLSWITCH_BURST_1H_CLASS_B", "5000000")
        ),
        "bus_url": os.environ.get(
            "AGENT_HUB_BUS_URL", "http://127.0.0.1:3051/bus/send"
        ),
        "bus_from": os.environ.get(
            "BUS_FROM", "871f8f6b-c1b8-4449-b3cc-2e87896427d8"
        ),
        "bus_to": os.environ.get(
            "BUS_TO", "f0ef8aab-ebe9-4df7-b29e-633bf2ec7164"
        ),
        "dry_run": os.environ.get("KILLSWITCH_DRY_RUN", "0") in ("1", "true", "yes"),
        "state_dir": state_dir,
        "state_file": state_dir / "state.json",
    }


def cf_request(
    token: str, method: str, url: str, body: dict | None = None
) -> tuple[int, dict]:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {"raw": raw[:2000]}
        return e.code, parsed


def managed_url(account: str, bucket: str) -> str:
    return f"{CF_API}/accounts/{account}/r2/buckets/{bucket}/domains/managed"


def get_managed(c: dict) -> dict:
    st, body = cf_request(c["token"], "GET", managed_url(c["account"], c["bucket"]))
    if st != 200 or not body.get("success"):
        raise RuntimeError(f"GET managed domain failed HTTP {st}: {body.get('errors')}")
    return body.get("result") or {}


def set_managed(c: dict, enabled: bool) -> dict:
    st, body = cf_request(
        c["token"],
        "PUT",
        managed_url(c["account"], c["bucket"]),
        {"enabled": enabled},
    )
    if st != 200 or not body.get("success"):
        raise RuntimeError(
            f"PUT managed domain enabled={enabled} failed HTTP {st}: {body.get('errors')}"
        )
    return body.get("result") or {}


def graphql_ops(c: dict, start: datetime, end: datetime) -> list[dict]:
    payload = {
        "query": GQL_OPS,
        "variables": {
            "accountTag": c["account"],
            "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "bucketName": c["bucket"],
        },
    }
    st, body = cf_request(c["token"], "POST", GQL_URL, payload)
    errors = body.get("errors") or []
    if errors:
        msgs = " | ".join(e.get("message", "") for e in errors)
        codes = [((e.get("extensions") or {}).get("code")) for e in errors]
        if "authz" in codes or "not authorized" in msgs.lower():
            raise AnalyticsUnauthorized(
                "GraphQL r2OperationsAdaptiveGroups returned authz. "
                "Add Account permission: Account Analytics Read "
                "(dashboard: My Profile → API Tokens → edit postup-terraform-r2 → "
                "Permissions → Account → Account Analytics → Read). "
                "Do not replace Workers R2 Storage Edit/Read or User API Tokens Edit. "
                f"raw={msgs}"
            )
        raise RuntimeError(f"GraphQL error HTTP {st}: {msgs}")
    accounts = (((body.get("data") or {}).get("viewer") or {}).get("accounts") or [])
    if not accounts:
        return []
    return accounts[0].get("r2OperationsAdaptiveGroups") or []


def summarize(groups: list[dict]) -> dict[str, Any]:
    mtd_b = 0
    by_hour: dict[str, int] = {}
    by_action: dict[str, int] = {}
    for g in groups:
        dims = g.get("dimensions") or {}
        action = dims.get("actionType") or ""
        hour = dims.get("datetimeHour") or ""
        n = int(((g.get("sum") or {}).get("requests")) or 0)
        by_action[action] = by_action.get(action, 0) + n
        if action in CLASS_B:
            mtd_b += n
            if hour:
                by_hour[hour] = by_hour.get(hour, 0) + n
    now = datetime.now(timezone.utc)
    cutoff_24h = (now - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    last_24h = sum(v for h, v in by_hour.items() if h >= cutoff_24h)
    burst_hour, burst_n = "", 0
    for h, v in by_hour.items():
        if v > burst_n:
            burst_hour, burst_n = h, v
    newest_hour = max(by_hour) if by_hour else None
    return {
        "class_b_mtd": mtd_b,
        "class_b_24h": last_24h,
        "burst_1h": burst_n,
        "burst_1h_at": burst_hour,
        "hours_observed": len(by_hour),
        "newest_hour": newest_hour,
        "by_action_class_b": {k: v for k, v in by_action.items() if k in CLASS_B},
        "queried_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def load_state(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2) + "\n")
    tmp.chmod(0o600)
    tmp.replace(path)


def bus_notify(c: dict, body: str) -> None:
    payload = {
        "from": c["bus_from"],
        "to": c["bus_to"],
        "type": "note",
        "body": body,
        "bypassSenderListen": True,
        "expectsReply": False,
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        c["bus_url"],
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode()
            log(f"bus notify HTTP {resp.status}")
            return
    except Exception as e:
        log(f"bus notify failed: {e}")


def cmd_status(c: dict) -> int:
    m = get_managed(c)
    log(
        f"bucket={c['bucket']} r2.dev enabled={m.get('enabled')} "
        f"domain={m.get('domain')}"
    )
    st = load_state(c["state_file"])
    if st:
        log(f"last_state={json.dumps(st)}")
    return 0


def cmd_disable(c: dict, reason: str = "manual") -> int:
    before = get_managed(c)
    log(f"disable start enabled={before.get('enabled')} reason={reason}")
    after = set_managed(c, False)
    log(f"disable done enabled={after.get('enabled')} domain={after.get('domain')}")
    if after.get("enabled"):
        log("ERROR: API returned enabled=true after disable")
        return 1
    return 0


def cmd_enable(c: dict) -> int:
    before = get_managed(c)
    log(f"enable start enabled={before.get('enabled')}")
    after = set_managed(c, True)
    log(f"enable done enabled={after.get('enabled')} domain={after.get('domain')}")
    if not after.get("enabled"):
        log("ERROR: API returned enabled=false after enable")
        return 1
    st = load_state(c["state_file"])
    st["tripped"] = False
    st["reenabled_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    save_state(c["state_file"], st)
    return 0


def cmd_check(c: dict, dry_run: bool) -> int:
    now = datetime.now(timezone.utc)
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    try:
        groups = graphql_ops(c, start, now)
    except AnalyticsUnauthorized as e:
        log(f"ANALYTICS_UNAUTHORIZED {e}")
        st = load_state(c["state_file"])
        if not st.get("notified_analytics_unauthorized"):
            bus_notify(
                c,
                "postup-r2-killswitch: cannot read R2 operation counts. "
                "GraphQL r2OperationsAdaptiveGroups returned authz. "
                "Martin needs to add Account → Account Analytics → Read on token "
                "postup-terraform-r2. Kill switch will not trip on spend until then. "
                "r2.dev managed domain API still works (Workers R2 Storage Edit). "
                "Planet upload held.",
            )
            st["notified_analytics_unauthorized"] = True
            save_state(c["state_file"], st)
        return 3

    stats = summarize(groups)
    lag = None
    if stats["newest_hour"]:
        try:
            newest = datetime.fromisoformat(
                stats["newest_hour"].replace("Z", "+00:00")
            )
            lag = int((now - newest).total_seconds())
        except Exception:
            lag = None
    stats["analytics_lag_seconds_lower_bound"] = lag
    log(
        f"counts class_b_mtd={stats['class_b_mtd']} class_b_24h={stats['class_b_24h']} "
        f"burst_1h={stats['burst_1h']} at={stats['burst_1h_at']} "
        f"mtd_thr={c['mtd_threshold']} burst_thr={c['burst_threshold']} "
        f"lag_s>={lag} dry_run={dry_run or c['dry_run']}"
    )

    reasons = []
    if stats["class_b_mtd"] > c["mtd_threshold"]:
        reasons.append(
            f"MTD Class B {stats['class_b_mtd']} > {c['mtd_threshold']}"
        )
    if stats["burst_1h"] > c["burst_threshold"]:
        reasons.append(
            f"1h Class B {stats['burst_1h']} at {stats['burst_1h_at']} "
            f"> {c['burst_threshold']}"
        )

    st = load_state(c["state_file"])
    st["last_check"] = stats
    save_state(c["state_file"], st)

    if not reasons:
        return 0

    reason = "; ".join(reasons)
    log(f"TRIP {reason}")
    if dry_run or c["dry_run"]:
        log("dry-run: would disable r2.dev managed domain")
        return 1

    managed = get_managed(c)
    already = managed.get("enabled") is False
    if not already:
        cmd_disable(c, reason=reason)

    notify = (
        "postup-r2-killswitch TRIPPED — r2.dev public access DISABLED for "
        f"bucket {c['bucket']}.\n"
        f"Reasons: {reason}\n"
        f"Class B MTD: {stats['class_b_mtd']}\n"
        f"Class B last 24h: {stats['class_b_24h']}\n"
        f"Class B max 1h: {stats['burst_1h']} at {stats['burst_1h_at']}\n"
        f"Thresholds: MTD {c['mtd_threshold']}, 1h burst {c['burst_threshold']}\n"
        f"domain: {managed.get('domain')}\n"
        "Re-enable is manual: "
        "python3 infra/r2/killswitch/killswitch.py enable\n"
        "Do not use AllowedOrigins *."
    )
    if not st.get("tripped"):
        bus_notify(c, notify)
    st["tripped"] = True
    st["trip_reason"] = reason
    st["tripped_at"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    save_state(c["state_file"], st)
    return 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="PostUp R2 r2.dev spend kill switch")
    p.add_argument(
        "command",
        nargs="?",
        default="check",
        choices=["check", "dry-run", "status", "disable", "enable"],
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not disable the managed domain",
    )
    args = p.parse_args(argv)
    try:
        c = cfg()
    except ConfigError as e:
        log(f"CONFIG {e}")
        return 2
    cmd = args.command
    if cmd == "dry-run":
        return cmd_check(c, dry_run=True)
    if cmd == "status":
        return cmd_status(c)
    if cmd == "disable":
        return cmd_disable(c)
    if cmd == "enable":
        return cmd_enable(c)
    return cmd_check(c, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
