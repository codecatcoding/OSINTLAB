#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CLOUDFLARED="$PROJECT_ROOT/Herramientas/cloudflared"
TUNNEL_NAME="${1:-osintlab-api}"
HOSTNAME="${2:-api.codecatcoding.com}"
API_PORT="${OSINTLAB_API_PORT:-8000}"
CONFIG_DIR="$HOME/.cloudflared"
CONFIG_FILE="$CONFIG_DIR/config.yml"

cd "$PROJECT_ROOT"
mkdir -p Logs Herramientas "$CONFIG_DIR"

if [ ! -x "$CLOUDFLARED" ]; then
  echo "[+] Descargando cloudflared..."
  curl -L --fail -o "$CLOUDFLARED" https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
  chmod +x "$CLOUDFLARED"
fi

if [ ! -x ./venv/bin/uvicorn ]; then
  echo "[+] Entorno virtual no encontrado. Ejecutando instalador..."
  bash Scripts/install_kali.sh
fi

if [ ! -f "$CONFIG_DIR/cert.pem" ]; then
  echo "[!] Falta iniciar sesion en Cloudflare."
  echo "[!] Se abrira o mostrara una URL. Autoriza el dominio codecatcoding.com en tu cuenta Cloudflare."
  "$CLOUDFLARED" tunnel login
fi

if ! "$CLOUDFLARED" tunnel info "$TUNNEL_NAME" >/dev/null 2>&1; then
  echo "[+] Creando tunnel $TUNNEL_NAME..."
  "$CLOUDFLARED" tunnel create "$TUNNEL_NAME"
else
  echo "[=] Tunnel $TUNNEL_NAME ya existe."
fi

TUNNEL_ID="$("$CLOUDFLARED" tunnel list --output json | python3 -c '
import json
import sys

name = sys.argv[1]
for item in json.load(sys.stdin):
    if item.get("name") == name:
        print(item.get("id") or item.get("uuid"))
        raise SystemExit(0)
raise SystemExit(f"No se encontro el tunnel {name!r}")
' "$TUNNEL_NAME")"

CREDENTIALS_FILE="$CONFIG_DIR/$TUNNEL_ID.json"

if [ ! -f "$CREDENTIALS_FILE" ]; then
  echo "[!] No encuentro las credenciales del tunnel: $CREDENTIALS_FILE"
  exit 1
fi

cat > "$CONFIG_FILE" <<YAML
tunnel: $TUNNEL_ID
credentials-file: $CREDENTIALS_FILE

ingress:
  - hostname: $HOSTNAME
    service: http://127.0.0.1:$API_PORT
  - service: http_status:404
YAML

echo "[+] Configuracion escrita en $CONFIG_FILE"

echo "[+] Creando ruta DNS $HOSTNAME -> $TUNNEL_NAME..."
"$CLOUDFLARED" tunnel route dns "$TUNNEL_NAME" "$HOSTNAME"

if ! pgrep -af "uvicorn web.main:app --host 127.0.0.1 --port $API_PORT" >/dev/null 2>&1; then
  echo "[+] Iniciando API local en 127.0.0.1:$API_PORT..."
  OSINTLAB_PUBLIC_MODE=true \
  OSINTLAB_ALLOWED_ORIGINS="https://codecatcoding.com,https://www.codecatcoding.com" \
  nohup ./venv/bin/uvicorn web.main:app --host 127.0.0.1 --port "$API_PORT" > Logs/api-cloudflare.log 2>&1 &
else
  echo "[=] API local ya esta activa."
fi

if ! pgrep -af "cloudflared.*tunnel.*run.*$TUNNEL_NAME" >/dev/null 2>&1; then
  echo "[+] Iniciando tunnel permanente en segundo plano..."
  nohup "$CLOUDFLARED" tunnel --config "$CONFIG_FILE" run "$TUNNEL_NAME" > Logs/cloudflare-named-tunnel.log 2>&1 &
else
  echo "[=] Tunnel permanente ya esta activo."
fi

sleep 3

echo
echo "[OK] Endpoint previsto:"
echo "https://$HOSTNAME/health"
echo
echo "Prueba:"
echo "curl -fsS https://$HOSTNAME/health"
