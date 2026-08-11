import os
from collections.abc import Callable, Sequence

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.utils.dns_lookup import resolve_domain
from app.utils.tool_manager import ToolManager
from app.utils.validators import is_domain, is_email, is_phone, is_username


class SearchRequest(BaseModel):
    """Entrada comun para busquedas OSINT."""

    target: str = Field(min_length=2, max_length=253)


class SearchResponse(BaseModel):
    """Respuesta normalizada de la API."""

    ok: bool
    tool: str
    target: str
    command: list[str] = []
    returncode: int = 0
    stdout: str = ""
    stderr: str = ""
    results: list[str] = []


API_TOKEN = os.getenv("OSINTLAB_API_TOKEN", "")
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "OSINTLAB_ALLOWED_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000,https://codecatcoding.com",
    ).split(",")
    if origin.strip()
]

app = FastAPI(title="OSINT LAB PRO API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-OSINTLAB-TOKEN"],
)


def require_access(
    request: Request,
    x_osintlab_token: str | None = Header(default=None),
) -> None:
    """Protege la API con token o limita el uso sin token a localhost."""

    if API_TOKEN:
        if x_osintlab_token != API_TOKEN:
            raise HTTPException(status_code=401, detail="Token invalido.")
        return

    client_host = request.client.host if request.client else ""

    if client_host not in {"127.0.0.1", "::1", "localhost"}:
        raise HTTPException(
            status_code=403,
            detail="Configura OSINTLAB_API_TOKEN antes de exponer la API publicamente.",
        )


@app.get("/health")
def health() -> dict[str, object]:
    """Estado basico de la API."""

    tools = {
        "sherlock": ToolManager.existe("sherlock"),
        "maigret": ToolManager.existe("maigret"),
        "holehe": ToolManager.existe("holehe"),
        "phoneinfoga": ToolManager.existe("phoneinfoga"),
        "theHarvester": ToolManager.existe("theHarvester"),
        "spiderfoot": ToolManager.existe("spiderfoot"),
        "recon-ng": ToolManager.existe("recon-ng"),
    }
    return {"ok": True, "tools": tools}


@app.post("/api/users/sherlock", response_model=SearchResponse, dependencies=[Depends(require_access)])
def users_sherlock(payload: SearchRequest) -> SearchResponse:
    target = _validate(payload.target, is_username, "Usuario no valido.")
    return _run("Sherlock", ["sherlock", target, "--print-found"], target, 240)


@app.post("/api/users/maigret", response_model=SearchResponse, dependencies=[Depends(require_access)])
def users_maigret(payload: SearchRequest) -> SearchResponse:
    target = _validate(payload.target, is_username, "Usuario no valido.")
    return _run("Maigret", ["maigret", target, "--no-color"], target, 300)


@app.post("/api/email/holehe", response_model=SearchResponse, dependencies=[Depends(require_access)])
def email_holehe(payload: SearchRequest) -> SearchResponse:
    target = _validate(payload.target, is_email, "Correo no valido.")
    return _run("Holehe", ["holehe", "--no-color", "--no-clear", "--only-used", target], target, 180)


@app.post("/api/phone/phoneinfoga", response_model=SearchResponse, dependencies=[Depends(require_access)])
def phone_phoneinfoga(payload: SearchRequest) -> SearchResponse:
    target = _validate(payload.target, is_phone, "Telefono no valido.")
    return _run("PhoneInfoga", ["phoneinfoga", "scan", "-n", target], target, 180)


@app.post("/api/domain/dns", response_model=SearchResponse, dependencies=[Depends(require_access)])
def domain_dns(payload: SearchRequest) -> SearchResponse:
    target = _validate(payload.target.lower(), is_domain, "Dominio no valido.")
    addresses, error = resolve_domain(target)
    return SearchResponse(
        ok=bool(addresses),
        tool="DNS",
        target=target,
        stdout="\n".join(addresses),
        stderr=error,
        results=addresses,
        returncode=0 if addresses else 1,
    )


@app.post("/api/domain/theharvester", response_model=SearchResponse, dependencies=[Depends(require_access)])
def domain_theharvester(payload: SearchRequest) -> SearchResponse:
    target = _validate(payload.target.lower(), is_domain, "Dominio no valido.")
    return _run("theHarvester", ["theHarvester", "-d", target, "-b", "duckduckgo", "-l", "100", "-q"], target, 240)


@app.post("/api/domain/spiderfoot", response_model=SearchResponse, dependencies=[Depends(require_access)])
def domain_spiderfoot(payload: SearchRequest) -> SearchResponse:
    target = _validate(payload.target.lower(), is_domain, "Dominio no valido.")
    return _run("SpiderFoot", ["spiderfoot", "-s", target, "-u", "passive", "-o", "tab", "-q"], target, 300)


def _run(tool: str, command: Sequence[str], target: str, timeout: int) -> SearchResponse:
    result = ToolManager.ejecutar_captura(command, timeout=timeout)
    return SearchResponse(
        ok=result.ok,
        tool=tool,
        target=target,
        command=result.command,
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )


def _validate(value: str, validator: Callable[[str], bool], message: str) -> str:
    target = value.strip()

    if not validator(target):
        raise HTTPException(status_code=422, detail=message)

    return target
