"""
Configuration and constants for DELTA BLACK.

Kept separate from logic so runtime behavior (timeouts, concurrency,
wordlist paths) can be tuned without touching the scanning code.
"""

from __future__ import annotations

import configparser
import os
from dataclasses import dataclass, field
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_WORDLIST = BASE_DIR / "wordlist.txt"
CONFIG_FILE = BASE_DIR / "config.ini"
WORDLIST_REMOTE_URL = (
    "https://github.com/danielmiessler/SecLists/raw/master/"
    "Discovery/DNS/subdomains-top1million-5000.txt"
)

TOOL_NAME = "DELTA BLACK"
TOOL_VERSION = "2.1.0"

# Upstream project this tool is derived from. Kept per the MIT license's
# attribution requirement -- do not remove.
UPSTREAM_PROJECT = "CloakQuest3r"
UPSTREAM_AUTHOR = "Spyboy"
UPSTREAM_URL = "https://github.com/spyboy-productions/CloakQuest3r"


@dataclass(frozen=True)
class ScanConfig:
    """Tunable parameters for a scan run.

    max_concurrency exists because the original tool spawned one raw
    thread per wordlist entry with no cap -- on a 5000-word list that's
    5000 simultaneous connections to the same target, which reads as a
    denial-of-service attempt to any WAF or the target's own infra, and
    gets the scanning IP blocked within seconds on most networks.
    """

    timeout_seconds: float = 8.0
    max_concurrency: int = 40
    retries: int = 1
    output_format: str = "none"  # "csv" | "none"
    output_path: str | None = None
    wordlist_path: Path = field(default_factory=lambda: DEFAULT_WORDLIST)
    verbose: bool = True


def read_securitytrails_key() -> str | None:
    """Read the SecurityTrails API key from config.ini, creating a
    template file on first run. Returns None if not configured.
    """
    parser = configparser.ConfigParser()

    if not CONFIG_FILE.exists():
        parser["DEFAULT"] = {"securitytrails_api_key": ""}
        with open(CONFIG_FILE, "w") as fh:
            parser.write(fh)
        return None

    parser.read(CONFIG_FILE)
    key = parser["DEFAULT"].get("securitytrails_api_key", "").strip()
    return key or None
