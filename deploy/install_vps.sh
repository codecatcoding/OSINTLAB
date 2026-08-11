#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/OSINTLAB"
REPO_URL="https://github.com/codecatcoding/OSINTLAB.git"

if [ "$(id -u)" -ne 0 ]; then
  echo "Ejecuta este instalador como root o con sudo."
  exit 1
fi

apt update
apt install -y git curl python3 python3-venv python3-pip nginx certbot python3-certbot-nginx libimage-exiftool-perl

if ! id osintlab >/dev/null 2>&1; then
  useradd --system --create-home --shell /usr/sbin/nologin osintlab
fi

if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" pull --ff-only
else
  git clone "$REPO_URL" "$APP_DIR"
fi

cp "$APP_DIR/.env.example" "$APP_DIR/.env"
chown -R osintlab:osintlab "$APP_DIR"

runuser -u osintlab -- bash "$APP_DIR/Scripts/install_kali.sh"

cp "$APP_DIR/deploy/osintlab-api.service" /etc/systemd/system/osintlab-api.service
cp "$APP_DIR/deploy/nginx-osintlab-api.conf" /etc/nginx/sites-available/osintlab-api
ln -sf /etc/nginx/sites-available/osintlab-api /etc/nginx/sites-enabled/osintlab-api

nginx -t
systemctl daemon-reload
systemctl enable --now osintlab-api
systemctl reload nginx

echo "Base instalada. Configura DNS para api.codecatcoding.com y luego ejecuta:"
echo "certbot --nginx -d api.codecatcoding.com"
