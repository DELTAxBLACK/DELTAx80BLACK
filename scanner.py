"""
DELTA BLACK subdomain enumeration.

Designed for domains you own or are explicitly authorized to test.
The scanner validates wordlists before network access, bounds concurrency,
and keeps all report bookkeeping in the coordinator thread.
"""
from __future__ import annotations

import logging
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

import requests

from config import ScanConfig
from network import CertificateInfo, get_ssl_certificate_info, resolve_ip

log = logging.getLogger("delta_black.scanner")

_LABEL_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")
_MAX_WORD_LENGTH = 200
_thread_local = threading.local()


@dataclass
class SubdomainResult:
    subdomain: str
    url: str
    status_code: int
    real_ip: str | None = None
    certificate: CertificateInfo | None = None


@dataclass
class ScanReport:
    target_domain: str
    subdomains_checked: int = 0
    results: list[SubdomainResult] = field(default_factory=list)
    elapsed_seconds: float = 0.0
    errors: int = 0
    wordlist_valid_entries: int = 0
    wordlist_skipped_entries: int = 0


@dataclass
class WordlistLoadResult:
    valid: list[str] = field(default_factory=list)
    total_lines: int = 0
    skipped_blank: int = 0
    skipped_comment: int = 0
    skipped_invalid: int = 0
    skipped_duplicate: int = 0

    @property
    def skipped_total(self) -> int:
        return self.skipped_blank + self.skipped_comment + self.skipped_invalid + self.skipped_duplicate


def _is_valid_subdomain_word(word: str) -> bool:
    if not word or len(word) > _MAX_WORD_LENGTH:
        return False
    return all(_LABEL_RE.fullmatch(label) for label in word.split("."))


def load_wordlist(path: Path) -> WordlistLoadResult:
    raw_lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    result = WordlistLoadResult(total_lines=len(raw_lines))
    seen: set[str] = set()

    for raw_line in raw_lines:
        line = raw_line.strip()
        if not line:
            result.skipped_blank += 1
            continue
        if line.startswith("#") or line.startswith(";"):
            result.skipped_comment += 1
            continue
        if not _is_valid_subdomain_word(line):
            result.skipped_invalid += 1
            log.debug("Skipped invalid wordlist entry: %r", line[:120])
            continue
        key = line.lower()
        if key in seen:
            result.skipped_duplicate += 1
            continue
        seen.add(key)
        result.valid.append(line)
    return result


def _get_session() -> requests.Session:
    session = getattr(_thread_local, "session", None)
    if session is None:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "DELTA BLACK/2.1 (authorized-security-testing)"
        })
        _thread_local.session = session
    return session


def _check_one(session: requests.Session | None, word: str, domain: str, timeout: float) -> SubdomainResult | None:
    if not _is_valid_subdomain_word(word):
        return None

    host = f"{word}.{domain}"
    url = f"https://{host}"
    try:
        response = (session or _get_session()).get(url, timeout=timeout, allow_redirects=True)
    except (requests.exceptions.RequestException, ValueError) as exc:
        log.debug("Probe failed for %s: %s", url, exc)
        return None

    if response.status_code != 200:
        return None

    return SubdomainResult(
        subdomain=word,
        url=url,
        status_code=response.status_code,
        real_ip=resolve_ip(host),
        certificate=get_ssl_certificate_info(host, timeout=timeout),
    )


def enumerate_subdomains(domain: str, cfg: ScanConfig, on_found=None) -> ScanReport:
    if not cfg.wordlist_path.exists():
        raise FileNotFoundError(
            f"Wordlist not found at {cfg.wordlist_path}. "
            "Run with --update-wordlist or pass --wordlist."
        )

    if cfg.max_concurrency < 1:
        raise ValueError("--concurrency must be at least 1")
    if cfg.timeout_seconds <= 0:
        raise ValueError("--timeout must be greater than 0")

    load_result = load_wordlist(cfg.wordlist_path)
    words = load_result.valid

    if not words:
        raise ValueError(
            f"No usable subdomain entries in {cfg.wordlist_path} "
            f"({load_result.total_lines} line(s) read, {load_result.skipped_total} "
            "skipped as blank/comment/invalid/duplicate). Run with "
            "--update-wordlist or pass --wordlist to a real list."
        )

    report = ScanReport(
        target_domain=domain,
        subdomains_checked=len(words),
        wordlist_valid_entries=len(words),
        wordlist_skipped_entries=load_result.skipped_total,
    )
    start = time.monotonic()

    with ThreadPoolExecutor(max_workers=cfg.max_concurrency, thread_name_prefix="recon") as pool:
        futures = {
            pool.submit(_check_one, None, word, domain, cfg.timeout_seconds): word
            for word in words
        }
        for future in as_completed(futures):
            word = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                report.errors += 1
                log.warning("Worker error on %s: %s", word, exc)
                continue
            if result is not None:
                report.results.append(result)
                if on_found:
                    on_found(result)

    report.elapsed_seconds = time.monotonic() - start
    return report
