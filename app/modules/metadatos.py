import mimetypes
from pathlib import Path

import exifread
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.ui.navigation import pausar
from app.utils.evidence_manager import EvidenceManager
from app.utils.investigation_runner import run_tool_and_save
from app.utils.tool_manager import ToolManager
from app.utils.validators import is_existing_file

console = Console()


def menu_metadatos() -> None:
    """Muestra el menu del modulo de metadatos."""

    while True:
        console.clear()

        tabla = Table(title="ANALISIS DE METADATOS")
        tabla.add_column("Opcion", justify="center", style="cyan")
        tabla.add_column("Accion", style="green")
        tabla.add_row("1", "Analizar archivo")
        tabla.add_row("0", "Volver")

        console.print(tabla)

        opcion = console.input("\n[bold yellow]Selecciona una opcion > [/]").strip()

        if opcion == "0":
            break

        if opcion == "1":
            _analizar_archivo()
            continue

        console.print("\n[bold red]Opcion no valida.[/bold red]")
        pausar()


def _analizar_archivo() -> None:
    file_path = _pedir_archivo()

    if file_path is None:
        return

    if ToolManager.existe("exiftool"):
        run_tool_and_save(
            tool_name="ExifTool",
            command=["exiftool", str(file_path)],
            target=str(file_path),
            title=f"exiftool-{file_path.name}",
            timeout=120,
        )
        return

    metadata = _extraer_metadata_python(file_path)
    evidence_path = EvidenceManager().add_note(
        "general",
        f"metadata-{file_path.name}",
        metadata,
    )

    console.print(Panel(metadata[:3500], title="Metadatos", border_style="green"))
    console.print(
        "\n[yellow]ExifTool no esta instalado; se uso extractor Python basico.[/yellow]"
    )
    console.print(f"[green]Evidencia guardada:[/green] {evidence_path}")
    pausar()


def _extraer_metadata_python(file_path: Path) -> str:
    stat = file_path.stat()
    mime_type, encoding = mimetypes.guess_type(file_path)
    lines = [
        f"# Metadatos: {file_path.name}",
        "",
        f"- Ruta: `{file_path}`",
        f"- Tamano bytes: `{stat.st_size}`",
        f"- MIME: `{mime_type or 'desconocido'}`",
        f"- Encoding: `{encoding or 'desconocido'}`",
        f"- Modificado: `{stat.st_mtime}`",
        "",
    ]

    if (mime_type or "").startswith("image/"):
        lines.extend(_leer_exif_imagen(file_path))

    return "\n".join(lines)


def _leer_exif_imagen(file_path: Path) -> list[str]:
    lines = ["## EXIF", ""]

    with file_path.open("rb") as image_file:
        tags = exifread.process_file(image_file, details=False)

    if not tags:
        lines.append("Sin etiquetas EXIF detectadas.")
        return lines

    for key, value in sorted(tags.items()):
        lines.append(f"- {key}: `{value}`")

    return lines


def _pedir_archivo() -> Path | None:
    raw_path = console.input("\nRuta del archivo: ").strip()

    if not is_existing_file(raw_path):
        console.print("\n[bold red]Archivo no encontrado.[/bold red]")
        pausar()
        return None

    return Path(raw_path).expanduser().resolve()
