"""Locate Java + tla2tools and run TLC. Cheap to rerun; no network."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

SPEC_DIR = Path(__file__).resolve().parents[1]
TLA_DIR = SPEC_DIR / "tla"
MODULE = TLA_DIR / "PostupLifecycle.tla"
REPO = SPEC_DIR.parents[1]  # postup-proto (or the worktree root)


def _mise_home() -> Path:
    return Path(os.environ.get("MISE_DATA_DIR", Path.home() / ".local/share/mise"))


def find_java() -> str:
    env = os.environ.get("JAVA")
    if env and Path(env).exists():
        return env
    home = os.environ.get("JAVA_HOME")
    if home:
        cand = Path(home) / "bin" / "java"
        if cand.exists():
            return str(cand)
    which = shutil.which("java")
    if which:
        return which
    # mise default install used by this prototype
    for p in sorted((_mise_home() / "installs" / "java").glob("*/bin/java")):
        return str(p)
    raise FileNotFoundError(
        "Java not found. Install with mise (java@temurin-25) or set JAVA / JAVA_HOME."
    )


def find_tla2tools() -> str:
    env = os.environ.get("TLA2TOOLS")
    if env and Path(env).exists():
        return env
    for p in sorted((_mise_home() / "installs").glob("http-tla2tools/*/tla2tools.jar")):
        return str(p)
    for p in (Path("/usr/local/share/tla2tools.jar"), Path("/opt/tla2tools.jar")):
        if p.exists():
            return str(p)
    raise FileNotFoundError(
        "tla2tools.jar not found. Install with mise (tla2tools v1.7.4) or set TLA2TOOLS."
    )


def run_tlc(cfg: Path, out_dir: Path, extra_invariants: list[str] | None = None) -> dict:
    """Run TLC on PostupLifecycle.tla with the given .cfg. Returns a result dict."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    use_cfg = Path(cfg)
    if extra_invariants:
        text = use_cfg.read_text()
        # append extra invariant names under INVARIANTS
        if "INVARIANTS" in text:
            text = text.replace("INVARIANTS\n", "INVARIANTS\n" + "".join(f"  {i}\n" for i in extra_invariants), 1)
        else:
            text += "\nINVARIANTS\n" + "".join(f"  {i}\n" for i in extra_invariants)
        use_cfg = out_dir / (cfg.stem + ".with-extra.cfg")
        use_cfg.write_text(text)
    log = out_dir / "tlc.out"
    java = find_java()
    jar = find_tla2tools()
    cmd = [
        java,
        "-XX:+UseParallelGC",
        "-cp",
        jar,
        "tlc2.TLC",
        "-config",
        str(use_cfg.resolve()),
        "-metadir",
        str((out_dir / "states").resolve()),
        "-workers",
        "auto",
        "-cleanup",
        str(MODULE.resolve()),
    ]
    proc = subprocess.run(cmd, cwd=str(TLA_DIR), capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    log.write_text(output)
    failed_inv = None
    for line in output.splitlines():
        # Error: Invariant Foo is violated.
        if "Invariant " in line and " is violated" in line:
            failed_inv = line.split("Invariant ", 1)[1].split(" is violated", 1)[0].strip()
            break
    success = proc.returncode == 0 and "Error:" not in output and failed_inv is None
    # TLC prints "Model checking completed. No error has been found." on success.
    if "No error has been found" in output:
        success = True
    if failed_inv or "Error:" in output and "No error has been found" not in output:
        success = False
    return {
        "ok": success,
        "returncode": proc.returncode,
        "failed_invariant": failed_inv,
        "log": str(log),
        "output": output,
        "cmd": cmd,
    }
