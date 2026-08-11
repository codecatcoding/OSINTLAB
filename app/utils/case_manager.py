import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.config.settings import AppPaths


class CaseManager:
    """Gestiona casos de investigacion OSINT."""

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or AppPaths.CASES

    def create_case(self, name: str) -> dict[str, Any]:
        """Crea un caso con metadatos basicos."""

        case_id = self._build_case_id(name)
        case_path = self.base_path / case_id
        case_path.mkdir(parents=True, exist_ok=False)

        metadata = {
            "id": case_id,
            "name": name.strip(),
            "status": "open",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        self._write_metadata(case_path, metadata)
        return metadata

    def list_cases(self) -> list[dict[str, Any]]:
        """Lista los casos existentes ordenados por fecha de creacion."""

        if not self.base_path.exists():
            return []

        cases: list[dict[str, Any]] = []

        for case_dir in sorted(self.base_path.iterdir()):
            metadata_path = case_dir / "case.json"
            if case_dir.is_dir() and metadata_path.exists():
                with metadata_path.open("r", encoding="utf-8") as metadata_file:
                    cases.append(json.load(metadata_file))

        return cases

    def _write_metadata(self, case_path: Path, metadata: dict[str, Any]) -> None:
        with (case_path / "case.json").open("w", encoding="utf-8") as metadata_file:
            json.dump(metadata, metadata_file, indent=2, ensure_ascii=False)

    @staticmethod
    def _build_case_id(name: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        slug = "".join(
            character.lower() if character.isalnum() else "-"
            for character in name.strip()
        ).strip("-")
        slug = "-".join(part for part in slug.split("-") if part)
        return f"{timestamp}-{slug or 'case'}"
