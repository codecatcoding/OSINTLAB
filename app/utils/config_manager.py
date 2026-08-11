import json
from pathlib import Path
from typing import Any

from app.config.settings import AppPaths, DEFAULT_CONFIG


class ConfigManager:
    """Gestiona la configuracion persistente de OSINT LAB PRO."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or AppPaths.CONFIG / "settings.json"

    def load(self) -> dict[str, Any]:
        """Carga la configuracion, creando valores por defecto si faltan."""

        if not self.path.exists():
            self.save(DEFAULT_CONFIG)
            return dict(DEFAULT_CONFIG)

        with self.path.open("r", encoding="utf-8") as config_file:
            data = json.load(config_file)

        return {**DEFAULT_CONFIG, **data}

    def save(self, data: dict[str, Any]) -> None:
        """Guarda la configuracion en disco."""

        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("w", encoding="utf-8") as config_file:
            json.dump(data, config_file, indent=2, ensure_ascii=False)
