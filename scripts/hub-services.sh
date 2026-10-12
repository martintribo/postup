#!/usr/bin/env bash
# Hub worktree services: local Docker Postgres + Vite. Never reads sibling .env / Neon.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -n "${DATABASE_URL:-}" && "$DATABASE_URL" == *neon* ]]; then
  echo "hub-services: refusing Neon DATABASE_URL from environment" >&2
  unset DATABASE_URL
fi

# Never source main checkout secrets
if [[ -f /home/main/dev/postup/.env ]]; then
  :
fi
unset POSTGRES_PASSWORD_FILE || true

PORT="${PORT:-15000}"
HOST="${HOST:-127.0.0.1}"
ID="${AGENT_HUB_WORKTREE_ID:-$(basename "$ROOT")}"
HUB_PG_PORT="${HUB_PG_PORT:-$((25000 + PORT - 15000))}"
export HUB_PG_PORT PORT HOST
COMPOSE_PROJECT="postup-wt-${ID}"
URL="postgres://postup:postup@127.0.0.1:${HUB_PG_PORT}/postup"

if ! command -v docker >/dev/null 2>&1; then
  echo "hub-services: docker not found (system postgres fallback not wired)" >&2
  exit 1
fi

echo "hub-services: postgres on 127.0.0.1:${HUB_PG_PORT} project=${COMPOSE_PROJECT}"
docker compose -p "$COMPOSE_PROJECT" -f docker-compose.hub.yml up -d --wait

ENV_LOCAL="$ROOT/.env.local"
touch "$ENV_LOCAL"
python3 - "$ENV_LOCAL" "$PORT" "$HOST" "$URL" <<'PY'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
port, host, url = sys.argv[2], sys.argv[3], sys.argv[4]
keys = {
    "PORT": port,
    "HOST": host,
    "VITE_PORT": port,
    "DATABASE_URL": url,
    "HUB_PG_PORT": str(int(port) - 15000 + 25000),
}
prev = path.read_text() if path.exists() else ""
seen = set()
out_lines = []
for line in prev.splitlines():
    if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
        out_lines.append(line)
        continue
    k = line.split("=", 1)[0].strip()
    if k in keys:
        out_lines.append(f'{k}={keys[k]}')
        seen.add(k)
    else:
        out_lines.append(line)
for k, v in keys.items():
    if k not in seen:
        out_lines.append(f"{k}={v}")
path.write_text("\n".join(out_lines).rstrip() + "\n")
PY

export DATABASE_URL="$URL"

if [[ ! -d node_modules ]]; then
  if command -v pnpm >/dev/null 2>&1; then
    pnpm install
  else
    npm install
  fi
fi

# No checked-in drizzle migrations — push schema to empty local DB.
# Use local bins (pnpm exec may fail on ignored esbuild builds).
./node_modules/.bin/drizzle-kit push --force \
  --dialect postgresql \
  --schema ./src/lib/server/db/schema.ts \
  --url "$DATABASE_URL"

mkdir -p "$ROOT/.hub"
PIDFILE="$ROOT/.hub/vite.pid"
LOG="$ROOT/.hub/vite.log"
if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "hub-services: vite already running pid=$(cat "$PIDFILE")"
else
  export HUB_VITE_HTTP=1
  nohup ./node_modules/.bin/vite dev --port "$PORT" --host "$HOST" --strictPort >"$LOG" 2>&1 &
  echo $! >"$PIDFILE"
  echo "hub-services: vite pid=$(cat "$PIDFILE") $HOST:$PORT"
fi

# Wait until something listens (HTTP or fail)
for i in $(seq 1 40); do
  if curl -sf -o /dev/null --max-time 1 "http://127.0.0.1:${PORT}/" || \
     curl -sk -o /dev/null --max-time 1 "https://127.0.0.1:${PORT}/"; then
    echo "hub-services: vite accepting on :${PORT}"
    exit 0
  fi
  sleep 0.5
done
echo "hub-services: vite started but not yet accepting (see $LOG)" >&2
tail -n 40 "$LOG" >&2 || true
exit 0
