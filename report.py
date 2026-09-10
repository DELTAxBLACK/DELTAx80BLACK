"""Optional CSV result export for DELTA BLACK."""

from __future__ import annotations

import csv
import logging
from pathlib import Path

from scanner import ScanReport

log = logging.getLogger("delta_black.report")


def write_csv(report: ScanReport, path: Path) -> Path:
    fieldnames = [
        "subdomain", "url", "status_code", "real_ip",
        "cert_common_name", "cert_issuer",
    ]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in report.results:
            writer.writerow({
                "subdomain": r.subdomain,
                "url": r.url,
                "status_code": r.status_code,
                "real_ip": r.real_ip or "",
                "cert_common_name": r.certificate.common_name if r.certificate else "",
                "cert_issuer": r.certificate.issuer if r.certificate else "",
            })
    log.info("Wrote CSV report to %s", path)
    return path


def export(report: ScanReport, fmt: str, path: str | None) -> Path | None:
    if fmt == "none":
        return None
    if fmt != "csv":
        raise ValueError(f"Unknown export format: {fmt!r}")
    if path is None:
        stamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"delta_black_{report.target_domain}_{stamp}.csv"
    return write_csv(report, Path(path))
