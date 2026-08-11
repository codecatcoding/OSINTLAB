import subprocess
import shutil
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from app.config.settings import AppPaths


@dataclass(frozen=True)
class CommandResult:
    """Resultado de una herramienta externa."""

    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False

    @property
    def ok(self) -> bool:
        """Indica si el comando termino correctamente."""

        return self.returncode == 0 and not self.timed_out


class ToolManager:
    """Punto unico para detectar y ejecutar herramientas externas."""

    @staticmethod
    def existe(comando: str) -> bool:
        """Comprueba si un comando existe en el sistema."""

        return ToolManager.resolver(comando) is not None

    @staticmethod
    def resolver(comando: str) -> Path | None:
        """Resuelve un comando desde PATH o desde el entorno virtual."""

        path = shutil.which(comando)

        if path is not None:
            return Path(path)

        venv_command = AppPaths.ROOT / "venv" / "bin" / comando

        if venv_command.exists():
            return venv_command

        return None

    @staticmethod
    def ejecutar(comando: Sequence[str]) -> bool:
        """Ejecuta un comando y devuelve True si termina correctamente."""

        return ToolManager.ejecutar_captura(comando).ok

    @staticmethod
    def ejecutar_captura(
        comando: Sequence[str],
        timeout: int = 180,
        cwd: Path | None = None,
    ) -> CommandResult:
        """Ejecuta un comando externo y captura stdout/stderr."""

        if not comando:
            return CommandResult([], 1, "", "Comando vacio")

        ejecutable = ToolManager.resolver(comando[0])

        if ejecutable is None:
            return CommandResult(list(comando), 127, "", f"Comando no encontrado: {comando[0]}")

        comando_resuelto = [str(ejecutable), *comando[1:]]

        try:
            resultado = subprocess.run(
                comando_resuelto,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
            )
            return CommandResult(
                command=comando_resuelto,
                returncode=resultado.returncode,
                stdout=resultado.stdout,
                stderr=resultado.stderr,
            )
        except subprocess.TimeoutExpired as error:
            return CommandResult(
                command=comando_resuelto,
                returncode=124,
                stdout=error.stdout or "",
                stderr=error.stderr or f"Timeout tras {timeout} segundos.",
                timed_out=True,
            )
        except OSError:
            return CommandResult(comando_resuelto, 1, "", "No se pudo ejecutar el comando.")

    @staticmethod
    def docker() -> bool:
        """Comprueba si Docker esta disponible."""

        return ToolManager.existe("docker")

    @staticmethod
    def sherlock() -> bool:
        """Comprueba si Sherlock esta disponible."""

        return ToolManager.existe("sherlock")

    @staticmethod
    def python() -> bool:
        """Comprueba si Python esta disponible."""

        return ToolManager.existe("python")

    @staticmethod
    def git() -> bool:
        """Comprueba si Git esta disponible."""

        return ToolManager.existe("git")

    @staticmethod
    def ejecutar_sherlock(usuario: str) -> bool:
        """Ejecuta Sherlock para un nombre de usuario."""

        return ToolManager.ejecutar(["sherlock", usuario, "--print-found"])
