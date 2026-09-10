"""
Network-facing operations: DNS resolution, CDN detection, SSL inspection.

Every function here that touches the network wraps its I/O in a
try/except that logs via the `logging` module rather than swallowing
the exception silently -- the original tool had several bare
`except: pass` / `except: None` blocks that made failures invisible.
"""

from __future__ import annotations

import logging
import socket
import ssl
from dataclasses import dataclass

import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend

log = logging.getLogger("delta_black.network")

CDN_SERVER_MARKERS = ("cloudflare",)
CDN_HEADER_MARKERS = ("cf-ray", "cloudflare")


@dataclass
class CertificateInfo:
    common_name: str
    issuer: str
    valid_from: str
    valid_until: str


def resolve_ip(host: str) -> str | None:
    """Resolve a hostname to its A-record IP. Returns None on
    NXDOMAIN or any resolution failure -- this is an expected, not
    exceptional, outcome for wordlist-based subdomain guessing, so it
    is logged at DEBUG rather than WARNING.
    """
    try:
        return socket.gethostbyname(host)
    except socket.gaierror as exc:
        log.debug("DNS resolution failed for %s: %s", host, exc)
        return None


def is_behind_cloudflare(domain: str, timeout: float = 8.0) -> bool:
    try:
        response = requests.head(f"https://{domain}", timeout=timeout)
    except requests.exceptions.RequestException as exc:
        log.warning("Could not reach %s to check CDN status: %s", domain, exc)
        return False

    headers = response.headers
    server_header = headers.get("server", "").lower()

    if any(marker in server_header for marker in CDN_SERVER_MARKERS):
        return True
    if any(marker in headers for marker in CDN_HEADER_MARKERS):
        return True
    return False


def detect_web_server(domain: str, timeout: float = 8.0) -> str:
    try:
        response = requests.head(f"https://{domain}", timeout=timeout)
        return response.headers.get("Server", "UNKNOWN").strip() or "UNKNOWN"
    except requests.exceptions.RequestException as exc:
        log.debug("Server header detection failed for %s: %s", domain, exc)
        return "UNKNOWN"


def get_ssl_certificate_info(host: str, timeout: float = 8.0) -> CertificateInfo | None:
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=timeout) as raw_sock:
            with context.wrap_socket(raw_sock, server_hostname=host) as tls_sock:
                der_cert = tls_sock.getpeercert(True)

        cert = x509.load_der_x509_certificate(der_cert, default_backend())
        common_name = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
        issuer = cert.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)

        return CertificateInfo(
            common_name=common_name[0].value if common_name else "unknown",
            issuer=issuer[0].value if issuer else "unknown",
            valid_from=cert.not_valid_before_utc.isoformat(),
            valid_until=cert.not_valid_after_utc.isoformat(),
        )
    except (OSError, ssl.SSLError, ValueError, IndexError) as exc:
        log.debug("SSL certificate retrieval failed for %s: %s", host, exc)
        return None
