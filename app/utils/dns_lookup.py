import json
import socket
from urllib.parse import urlencode
from urllib.request import urlopen

import dns.resolver


def resolve_domain(domain: str) -> tuple[list[str], str]:
    """Resuelve direcciones A con fallback DNS-over-HTTPS."""

    try:
        addresses = sorted({info[4][0] for info in socket.getaddrinfo(domain, None)})
    except socket.gaierror as error:
        socket_error = str(error)
    else:
        return addresses, ""

    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ["1.1.1.1", "8.8.8.8"]
    resolver.timeout = 3
    resolver.lifetime = 6

    try:
        answers = resolver.resolve(domain, "A")
    except Exception as error:
        doh_addresses, doh_error = _resolve_doh(domain)

        if doh_addresses:
            return doh_addresses, ""

        return [], f"{socket_error}; fallback DNS: {error}; fallback DoH: {doh_error}"

    return sorted({answer.address for answer in answers}), ""


def _resolve_doh(domain: str) -> tuple[list[str], str]:
    query = urlencode({"name": domain, "type": "A"})
    url = f"https://dns.google/resolve?{query}"

    try:
        with urlopen(url, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as error:
        return [], str(error)

    answers = payload.get("Answer", [])
    addresses = sorted(
        {
            answer.get("data", "")
            for answer in answers
            if answer.get("type") == 1 and answer.get("data")
        }
    )

    return addresses, ""
