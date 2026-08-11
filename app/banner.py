from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel

console = Console()


def mostrar_banner() -> None:
    """Muestra el banner principal de OSINT LAB PRO."""

    fig = Figlet(font="slant")
    texto = fig.renderText("OSINT LAB")

    console.print(f"[cyan]{texto}[/cyan]")
    console.print(
        Panel.fit(
            "[bold bright_green]OSINT LAB PRO v1.0[/bold bright_green]\n"
            "[bold cyan]Powered by CodeCatCoding[/bold cyan]\n"
            "[white]Professional OSINT Framework[/white]",
            title="[bold blue]Framework[/bold blue]",
            subtitle="[bold green]Python Edition[/bold green]",
            border_style="bright_blue",
        )
    )
