"""
Historical IP address lookups against third-party sources
(ViewDNS scraping, SecurityTrails API).

Kept separate from the core scanner so a source going down or
changing its markup doesn't touch scanning logic -- both original
implementations of these had bare `except: None` blocks; here each
failure mode is caught specifically and logged.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from config import read_securitytrails_key

log = logging.getLogger("delta_black.historical")

VIEWDNS_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36"
)


@dataclass
class HistoricalRecord:
    ip: str
    source: str
    location: str | None = None
    owner: str | None = None
    first_seen: str | None = None
    last_seen: str | None = None
    organizations: str | None = None


def fetch_viewdns_history(domain: str, timeout: float = 10.0) -> list[HistoricalRecord] | None:
    """Scrape ViewDNS's IP history page for `domain`.

    Returns `None` when the source itself couldn't be checked --
    network error, timeout, or a non-2xx response including the 403
    ViewDNS returns when it blocks or rate-limits a client. That is a
    statement about ViewDNS's availability, not about the domain, and
    must not be read as "no historical IP exists".

    Returns `[]` only when ViewDNS was actually reached and genuinely
    has no history table for the domain -- a real, checked negative.
    """
    url = f"https://viewdns.info/iphistory/?domain={domain}"
    headers = {
        "User-Agent": VIEWDNS_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else None
        if status == 403:
            log.warning(
                "ViewDNS blocked the request for %s (403) -- source "
                "unavailable, not evidence of no historical IP", domain,
            )
        else:
            log.warning("ViewDNS returned HTTP %s for %s: %s", status, domain, exc)
        return None
    except requests.exceptions.RequestException as exc:
        log.warning("ViewDNS lookup failed for %s: %s", domain, exc)
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"border": "1"})
    if table is None:
        log.debug("ViewDNS returned no history table for %s", domain)
        return []

    records: list[HistoricalRecord] = []
    for row in table.find_all("tr")[2:]:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue
        records.append(
            HistoricalRecord(
                ip=cols[0].get_text(strip=True),
                source="viewdns",
                location=cols[1].get_text(strip=True),
                owner=cols[2].get_text(strip=True),
                last_seen=cols[3].get_text(strip=True),
            )
        )
    return records


def fetch_securitytrails_history(domain: str, timeout: float = 10.0) -> list[HistoricalRecord]:
    api_key = read_securitytrails_key()
    if not api_key:
        log.info("No SecurityTrails API key configured; skipping that source.")
        return []

    url = f"https://api.securitytrails.com/v1/history/{domain}/dns/a"
    headers = {"accept": "application/json", "APIKEY": api_key}

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as exc:
        log.warning("SecurityTrails lookup failed for %s: %s", domain, exc)
        return []
    except ValueError as exc:
        log.warning("SecurityTrails returned invalid JSON for %s: %s", domain, exc)
        return []

    records: list[HistoricalRecord] = []
    for record in data.get("records", []):
        values = record.get("values") or [{}]
        orgs = record.get("organizations") or []
        records.append(
            HistoricalRecord(
                ip=values[0].get("ip", "unknown"),
                source="securitytrails",
                first_seen=record.get("first_seen"),
                last_seen=record.get("last_seen"),
                organizations=orgs[0] if orgs else None,
            )
        )
    return records
