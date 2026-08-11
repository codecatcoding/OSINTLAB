# Deploy OSINT LAB PRO API

This API must run on a Linux server. A static Elementor widget cannot execute Sherlock, Maigret, PhoneInfoga, SpiderFoot or Recon-ng by itself.

Recommended public endpoint:

```text
https://api.codecatcoding.com
```

## VPS Install

On a fresh Debian/Ubuntu/Kali server:

```bash
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/codecatcoding/OSINTLAB/main/deploy/install_vps.sh)"
```

Then point the DNS record:

```text
api.codecatcoding.com -> VPS_PUBLIC_IP
```

Finally enable HTTPS:

```bash
sudo certbot --nginx -d api.codecatcoding.com
```

## Free Without VPS

If you do not have a VPS, use Cloudflare Tunnel instead. It publishes the Kali local API through HTTPS without opening ports:

```bash
cd ~/OSINTLAB
bash Scripts/setup_cloudflare_tunnel.sh osintlab-api api.codecatcoding.com
```

See `deploy/README_CLOUDFLARE_TUNNEL.md`.

## Environment

Edit:

```bash
sudo nano /opt/OSINTLAB/.env
sudo systemctl restart osintlab-api
```

Public website mode:

```env
OSINTLAB_PUBLIC_MODE=true
OSINTLAB_ALLOWED_ORIGINS=https://codecatcoding.com,https://www.codecatcoding.com
OSINTLAB_RATE_LIMIT_REQUESTS=20
OSINTLAB_RATE_LIMIT_WINDOW=60
```

Private token mode:

```env
OSINTLAB_PUBLIC_MODE=false
OSINTLAB_API_TOKEN=change-this-token
```

Do not put a private API token in frontend HTML.
