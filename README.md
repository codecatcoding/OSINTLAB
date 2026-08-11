# OSINT LAB PRO

Professional OSINT framework for Linux and Kali Linux, built as a modular Python terminal application.

## Features

- Rich terminal UI.
- Central menu router.
- Tool status detection.
- Case, evidence, report and configuration managers.
- Sherlock, Maigret, Holehe, PhoneInfoga, SpiderFoot, Recon-ng and theHarvester integration.
- Automatic Markdown evidence capture for tool output.

## Install On Linux

### 1. Install system dependencies

Debian, Ubuntu, Kali and derivatives:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
```

Optional but recommended on Kali:

```bash
sudo apt install -y libimage-exiftool-perl
```

### 2. Clone the project

```bash
git clone https://github.com/codecatcoding/OSINTLAB.git ~/OSINTLAB
cd ~/OSINTLAB
```

### 3. Run the installer

```bash
bash Scripts/install_kali.sh
```

The installer creates the virtual environment, installs Python dependencies, downloads local tool integrations and prepares the command wrappers.

### 4. Start OSINT LAB PRO

```bash
./venv/bin/python run.py
```

## Quick Kali Install

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip libimage-exiftool-perl
git clone https://github.com/codecatcoding/OSINTLAB.git ~/OSINTLAB
cd ~/OSINTLAB
bash Scripts/install_kali.sh
./venv/bin/python run.py
```

## Run

```bash
cd ~/OSINTLAB
./venv/bin/python run.py
```

Or:

```bash
cd ~/OSINTLAB
source venv/bin/activate
python run.py
```

## Web API

OSINT LAB PRO also includes a local FastAPI backend that can be connected to a website widget.

Local development:

```bash
cd ~/OSINTLAB
./venv/bin/python run_web.py
```

The API starts at:

```text
http://127.0.0.1:8000
```

Public deployment should always use a token and HTTPS:

```bash
export OSINTLAB_API_TOKEN="change-this-token"
export OSINTLAB_ALLOWED_ORIGINS="https://codecatcoding.com"
./venv/bin/uvicorn web.main:app --host 127.0.0.1 --port 8000
```

Recommended production setup:

- Run the API behind Nginx or another reverse proxy.
- Expose it as `https://api.codecatcoding.com`.
- Protect it with `OSINTLAB_API_TOKEN`.
- Add rate limiting before exposing it publicly.

VPS deployment files are included in `deploy/`.

```bash
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/codecatcoding/OSINTLAB/main/deploy/install_vps.sh)"
sudo certbot --nginx -d api.codecatcoding.com
```

Free without VPS, using Cloudflare Tunnel:

```bash
cd ~/OSINTLAB
bash Scripts/setup_cloudflare_tunnel.sh osintlab-api api.codecatcoding.com
```

Detailed guide: `deploy/README_CLOUDFLARE_TUNNEL.md`.

## Paid PDF Reports

The repository includes a WordPress/WooCommerce plugin for paid reports:

```text
wordpress/osintlab-reports/
```

It creates:

- Product: `Informe OSINT LAB PRO`
- Price: `10 EUR`
- Coupon: `code2026` with 100% discount for that product

The Elementor widget can collect search results, send them to WooCommerce checkout and unlock a PDF report after payment.

## Update

```bash
cd ~/OSINTLAB
git pull
bash Scripts/install_kali.sh
./venv/bin/python run.py
```

## Project Layout

```text
app/
  modules/
  utils/
  config/
  ui/
run.py
Scripts/install_kali.sh
requirements.txt
```

## Operational Notes

Use this framework only on targets you own or are authorized to investigate.

Evidence, cases, logs, reports, virtual environments and locally cloned external tools are intentionally ignored by Git.
