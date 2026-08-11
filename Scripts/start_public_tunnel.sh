#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CLOUDFLARED="$PROJECT_ROOT/Herramientas/cloudflared"

cd "$PROJECT_ROOT"
mkdir -p Logs Herramientas

if [ ! -x "$CLOUDFLARED" ]; then
  curl -L --fail -o "$CLOUDFLARED" https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
  chmod +x "$CLOUDFLARED"
fi

OSINTLAB_PUBLIC_MODE=true \
OSINTLAB_ALLOWED_ORIGINS="https://codecatcoding.com,https://www.codecatcoding.com" \
nohup ./venv/bin/uvicorn web.main:app --host 127.0.0.1 --port 8000 > Logs/api-public.log 2>&1 &

nohup "$CLOUDFLARED" tunnel --url http://127.0.0.1:8000 > Logs/cloudflared.log 2>&1 &

sleep 10
grep -Eo "https://[-a-zA-Z0-9]+\\.trycloudflare\\.com" Logs/cloudflared.log | tail -1
