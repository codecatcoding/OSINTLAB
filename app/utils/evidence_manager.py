from datetime import datetime
from pathlib import Path

from app.config.settings import AppPaths
from app.utils.tool_manager import CommandResult


class EvidenceManager:
    """Gestiona evidencias asociadas a casos."""

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or AppPaths.EVIDENCE

    def create_evidence_folder(self, case_id: str) -> Path:
        """Crea y devuelve la carpeta de evidencias de un caso."""

        evidence_path = self.base_path / case_id
        evidence_path.mkdir(parents=True, exist_ok=True)
        return evidence_path

    def add_note(self, case_id: str, title: str, content: str) -> Path:
        """Guarda una nota de evidencia en Markdown."""

        evidence_path = self.create_evidence_folder(case_id)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}-{self._slug(title)}.md"
        note_path = evidence_path / filename
        note_path.write_text(content, encoding="utf-8")
        return note_path

    def add_command_result(
        self,
        case_id: str,
        title: str,
        target: str,
        result: CommandResult,
    ) -> Path:
        """Guarda la salida de una herramienta externa como evidencia."""

        command = " ".join(result.command)
        status = "OK" if result.ok else "ERROR"
        content = (
            f"# {title}\n\n"
            f"- Objetivo: `{target}`\n"
            f"- Estado: `{status}`\n"
            f"- Codigo de salida: `{result.returncode}`\n"
            f"- Timeout: `{result.timed_out}`\n"
            f"- Comando: `{command}`\n"
            f"- Fecha: `{datetime.now().isoformat(timespec='seconds')}`\n\n"
            "## STDOUT\n\n"
            "```text\n"
            f"{result.stdout.strip()}\n"
            "```\n\n"
            "## STDERR\n\n"
            "```text\n"
            f"{result.stderr.strip()}\n"
            "```\n"
        )
        return self.add_note(case_id, title, content)

    @staticmethod
    def _slug(value: str) -> str:
        slug = "".join(
            character.lower() if character.isalnum() else "-"
            for character in value.strip()
        ).strip("-")
        return "-".join(part for part in slug.split("-") if part) or "evidence"
