# Cloudflare Tunnel Gratis

Esta es la opcion recomendada si no tienes VPS y quieres que la web use un endpoint fijo:

```text
https://api.codecatcoding.com
```

Hostinger solo aloja la web. Para ejecutar Sherlock, Maigret, PhoneInfoga, SpiderFoot o Recon-ng hace falta un backend Linux activo. Con Cloudflare Tunnel, Kali ejecuta la API localmente y Cloudflare la publica por HTTPS sin abrir puertos ni pagar VPS.

## Requisitos

- Cuenta gratis de Cloudflare.
- El dominio `codecatcoding.com` anadido en Cloudflare.
- Nameservers del dominio cambiados desde Hostinger a los nameservers que indique Cloudflare.
- Kali encendido mientras quieras que la API funcione.

## Instalacion

En Kali:

```bash
cd ~/OSINTLAB
git pull
bash Scripts/install_kali.sh
bash Scripts/setup_cloudflare_tunnel.sh osintlab-api api.codecatcoding.com
```

La primera vez `cloudflared` pedira iniciar sesion. Abre la URL que muestre, entra en Cloudflare y autoriza el dominio `codecatcoding.com`.

Cuando termine, prueba:

```bash
curl -fsS https://api.codecatcoding.com/health
```

Si devuelve JSON con `"ok": true`, Elementor puede usar:

```html
data-api-base="https://api.codecatcoding.com"
```

## Modo Temporal

Si todavia no has movido DNS a Cloudflare, usa el tunnel temporal:

```bash
cd ~/OSINTLAB
bash Scripts/start_public_tunnel.sh
```

Ese comando devuelve una URL parecida a:

```text
https://algo-aleatorio.trycloudflare.com
```

Pegala en el widget de Elementor como `data-api-base`. Esta URL no es permanente: puede cambiar al reiniciar el tunnel.

## Servicio Persistente

Para dejarlo mas estable, instala el servicio de Cloudflare despues de confirmar que el tunnel funciona:

```bash
sudo ~/OSINTLAB/Herramientas/cloudflared service install
sudo systemctl enable --now cloudflared
```

Comprueba estado:

```bash
systemctl status cloudflared --no-pager
```

La API local tambien debe quedar activa. Si prefieres servicio systemd para la API, usa el archivo de ejemplo:

```bash
sudo cp deploy/osintlab-api.service /etc/systemd/system/osintlab-api.service
sudo systemctl daemon-reload
sudo systemctl enable --now osintlab-api
```
