# OSINT LAB PRO

Professional OSINT framework for Kali Linux, built as a modular Python terminal application.

## Features

- Rich terminal UI.
- Central menu router.
- Tool status detection.
- Case, evidence, report and configuration managers.
- Sherlock, Maigret, Holehe, PhoneInfoga, SpiderFoot, Recon-ng and theHarvester integration.
- Automatic Markdown evidence capture for tool output.

## Install On Kali

```bash
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
