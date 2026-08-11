from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class AppPaths:
    """Rutas principales del proyecto."""

    ROOT = PROJECT_ROOT
    BACKUPS = ROOT / "Backups"
    CASES = ROOT / "Casos"
    CONFIG = ROOT / "Configuracion"
    EVIDENCE = ROOT / "Evidencias"
    TOOLS = ROOT / "Herramientas"
    REPORTS = ROOT / "Informes"
    LOGS = ROOT / "Logs"
    TEMPLATES = ROOT / "Plantillas"
    SCRIPTS = ROOT / "Scripts"
    WORDLISTS = ROOT / "Wordlists"


APP_NAME = "OSINT LAB PRO"
APP_VERSION = "1.0"

EXTERNAL_TOOLS: dict[str, str] = {
    "Python": "python",
    "Git": "git",
    "Docker": "docker",
    "Sherlock": "sherlock",
    "PhoneInfoga": "phoneinfoga",
    "Maigret": "maigret",
    "Holehe": "holehe",
    "theHarvester": "theHarvester",
    "SpiderFoot": "spiderfoot",
    "Recon-ng": "recon-ng",
}

DEFAULT_CONFIG: dict[str, object] = {
    "app_name": APP_NAME,
    "version": APP_VERSION,
    "author": "CodeCatCoding",
    "default_case_status": "open",
}
