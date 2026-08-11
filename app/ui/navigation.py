from rich.console import Console

console = Console()


def pausar(mensaje: str = "\nPulsa ENTER para continuar...") -> None:
    """Pausa la navegacion hasta que el usuario pulse ENTER."""

    console.input(mensaje)


def mostrar_en_desarrollo(nombre: str) -> None:
    """Muestra un aviso consistente para modulos aun no implementados."""

    console.print(f"\n[yellow]Modulo de {nombre} en desarrollo...[/yellow]")
    pausar()
