from datetime import datetime
from pathlib import Path

from app.config.settings import AppPaths


class ReportManager:
    """Gestiona informes generados por el framework."""

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or AppPaths.REPORTS

    def list_reports(self) -> list[Path]:
        """Lista los informes disponibles."""

        if not self.base_path.exists():
            return []

        return sorted(self.base_path.glob("*.md"))

    def create_basic_report(self, case_id: str, title: str) -> Path:
        """Crea una plantilla inicial de informe en Markdown."""

        self.base_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_path = self.base_path / f"{timestamp}-{case_id}.md"
        content = (
            f"# {title}\n\n"
            f"- Caso: {case_id}\n"
            f"- Fecha: {datetime.now().isoformat(timespec='seconds')}\n\n"
            "## Resumen\n\n"
            "Pendiente.\n\n"
            "## Evidencias\n\n"
            "Pendiente.\n\n"
            "## Conclusiones\n\n"
            "Pendiente.\n"
        )
        report_path.write_text(content, encoding="utf-8")
        return report_path

    def create_report_from_evidence(
        self,
        case_id: str,
        title: str,
        evidence_path: Path | None = None,
    ) -> Path:
        """Crea un informe Markdown consolidando evidencias de un caso."""

        self.base_path.mkdir(parents=True, exist_ok=True)
        evidence_base = evidence_path or AppPaths.EVIDENCE / case_id
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_path = self.base_path / f"{timestamp}-{case_id}-evidencias.md"

        lines = [
            f"# {title}",
            "",
            f"- Caso: `{case_id}`",
            f"- Fecha: `{datetime.now().isoformat(timespec='seconds')}`",
            "",
            "## Evidencias consolidadas",
            "",
        ]

        if not evidence_base.exists():
            lines.append("No se encontraron evidencias para este caso.")
        else:
            for evidence_file in sorted(evidence_base.glob("*.md")):
                lines.extend(
                    [
                        f"### {evidence_file.name}",
                        "",
                        evidence_file.read_text(encoding="utf-8"),
                        "",
                    ]
                )

        report_path.write_text("\n".join(lines), encoding="utf-8")
        return report_path
