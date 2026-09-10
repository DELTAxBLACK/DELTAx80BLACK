#!/usr/bin/env python3
"""
DELTA BLACK -- CDN-origin exposure scanner.

Checks whether a domain sits behind Cloudflare, then attempts to
locate the real origin IP via historical DNS records and subdomain
enumeration (subdomains are often misconfigured to skip the CDN).

For use against domains you own or are authorized to test. Derived
from CloakQuest3r by Spyboy (https://github.com/spyboy-productions/CloakQuest3r),
MIT licensed -- see LICENSE.
"""

from __future__ import annotations

import argparse
import logging
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:  # graceful fallback when optional terminal coloring is unavailable
    class _NoColor:
        RESET_ALL = BRIGHT = DIM = CYAN = YELLOW = GREEN = RED = ""
    Fore = Style = _NoColor()
    def colorama_init(*args, **kwargs):
        return None


from config import (
    DEFAULT_WORDLIST,
    TOOL_NAME,
    TOOL_VERSION,
    UPSTREAM_AUTHOR,
    UPSTREAM_PROJECT,
    UPSTREAM_URL,
    WORDLIST_REMOTE_URL,
    ScanConfig,
)
from historical import fetch_securitytrails_history, fetch_viewdns_history
from network import detect_web_server, is_behind_cloudflare, resolve_ip
from report import export
from scanner import SubdomainResult, enumerate_subdomains, load_wordlist

log = logging.getLogger("delta_black")

# Static banner; keep this as a module constant so build_banner() cannot
# fail with NameError when the tool is launched directly on Termux.
ascii_banner = r"""                                       #::::             :::-*
                                       *=                     :+
                                       #.                      *
                                      +=.                      =-
                                     #.                        *
                                    :+                         *
                                    **.                        --
                               .::. @%:                         *
                            -+-.    *:                          +      ::
                           =+      .=                           .       -:
                           :+                                           -.
                            .-                                         :.
                              .:.           ...........              .
                                  .:.       .........
                                       ..::::::::.........

                                      *                       +
                                   ..  *                     -
                                :=     -                   .     :.
                                *-     =                     -     .=
                              -#-      %:                   .%       *:
                             **.       +*+.               .=+*       :*=
                           .#+  .      -==**-           -++===        .++
                    .:-:. -*-           +===*#*:     -#%*+===          .-*. .:::
                .:.      --.            :+====@@+   +@@*====:            :*: 
                        +-...            -+=+%+       *%+==-             .:#-
                            ...::         =**  .     : .**=
                              ...          -   ::   -:   -          .::
                           ::.                  *  .*                  :=:
                         ==              .      +   *                    .#.
                          ::             .     =:   -:                   -
                            -                  *     +                 .-
                             :                 =     =                :.
                                               .     :               .
                                              .       .
                                              .       ."""


def build_banner() -> str:
    return (
        f"{Fore.CYAN}{Style.BRIGHT}{ascii_banner}{Style.RESET_ALL}"
        f"\n{Fore.CYAN}{Style.BRIGHT}{TOOL_NAME}{Style.RESET_ALL} v{TOOL_VERSION}\n"
        f"{Fore.YELLOW}Authorized CDN / DNS exposure assessment tool.{Style.RESET_ALL}\n"
        f"{Style.DIM}Derived from {UPSTREAM_PROJECT} by {UPSTREAM_AUTHOR} "
        f"({UPSTREAM_URL}), MIT licensed.{Style.RESET_ALL}\n"
    )


def normalize_domain(raw: str) -> str:
    value = raw.strip()
    parsed = urlparse(value if "://" in value else f"https://{value}")
    domain = parsed.hostname or ""
    domain = domain.rstrip(".").lower()
    if not domain or any(ch.isspace() for ch in domain):
        raise ValueError(f"Invalid domain: {raw!r}")
    return domain


def update_wordlist(target_path: Path) -> None:
    print(f"{Fore.GREEN}[+] {Fore.CYAN}Fetching updated wordlist from SecLists...{Style.RESET_ALL}")
    try:
        urllib.request.urlretrieve(WORDLIST_REMOTE_URL, target_path)
        print(f"{Fore.GREEN}[+] Wordlist saved to {target_path}{Style.RESET_ALL}")
    except OSError as exc:
        log.error("Wordlist download failed: %s", exc)
        print(f"{Fore.RED}[!] Download failed: {exc}{Style.RESET_ALL}")
        sys.exit(1)


def print_found(result: SubdomainResult) -> None:
    line = f"{Fore.GREEN}  \u2514\u2500\u25b8 {result.url}{Style.RESET_ALL}"
    if result.real_ip:
        line += f"  {Fore.RED}[{result.real_ip}]{Style.RESET_ALL}"
    print(line)


def run(domain: str, cfg: ScanConfig, args: argparse.Namespace) -> int:
    print(build_banner())

    visible_ip = resolve_ip(domain)
    behind_cdn = is_behind_cloudflare(domain, timeout=cfg.timeout_seconds)

    print(f"{Fore.CYAN}[*] Target:{Style.RESET_ALL}       {domain}")
    print(f"{Fore.CYAN}[*] Visible IP:{Style.RESET_ALL}   {visible_ip or 'unresolved'}")
    print(f"{Fore.CYAN}[*] Behind CDN:{Style.RESET_ALL}   {'yes (Cloudflare)' if behind_cdn else 'no'}")

    if not behind_cdn:
        server = detect_web_server(domain, timeout=cfg.timeout_seconds)
        print(f"{Fore.CYAN}[*] Server header:{Style.RESET_ALL} {server}")
        if not args.yes:
            proceed = input(
                f"\n{Fore.YELLOW}Not behind a known CDN -- historical/subdomain "
                f"lookups may be unnecessary. Continue anyway? (y/N): {Style.RESET_ALL}"
            ).strip().lower()
            if proceed != "y":
                print(f"{Fore.RED}Aborted.{Style.RESET_ALL}")
                return 0

    if not args.skip_historical:
        print(f"\n{Fore.YELLOW}[+] Checking historical IP sources...{Style.RESET_ALL}")

        viewdns_records = fetch_viewdns_history(domain, timeout=cfg.timeout_seconds)
        if viewdns_records is None:
            print(
                f"{Fore.YELLOW}  [ViewDNS] source unavailable (blocked/unreachable) "
                f"-- not evidence of no historical IP{Style.RESET_ALL}"
            )
        elif not viewdns_records:
            print(f"{Fore.CYAN}  [ViewDNS] no historical records found{Style.RESET_ALL}")
        else:
            for record in viewdns_records:
                print(
                    f"{Fore.RED}  [ViewDNS] {record.ip}{Style.RESET_ALL} "
                    f"- {record.owner or 'unknown owner'} ({record.last_seen or '?'})"
                )

        st_records = fetch_securitytrails_history(domain, timeout=cfg.timeout_seconds)
        if not st_records:
            print(f"{Fore.CYAN}  [SecurityTrails] no historical records found{Style.RESET_ALL}")
        else:
            for record in st_records:
                print(
                    f"{Fore.RED}  [SecurityTrails] {record.ip}{Style.RESET_ALL} "
                    f"- {record.organizations or 'unknown org'} "
                    f"(first: {record.first_seen}, last: {record.last_seen})"
                )

    if args.skip_subdomains:
        return 0

    if not cfg.wordlist_path.exists():
        print(
            f"\n{Fore.YELLOW}[!] Wordlist not found at {cfg.wordlist_path}; "
            f"fetching default...{Style.RESET_ALL}"
        )
        update_wordlist(cfg.wordlist_path)
    else:
        try:
            wl_status = load_wordlist(cfg.wordlist_path)
            if not wl_status.valid:
                print(
                    f"\n{Fore.YELLOW}[!] Wordlist contains no usable entries; "
                    f"refreshing it from SecLists...{Style.RESET_ALL}"
                )
                update_wordlist(cfg.wordlist_path)
        except OSError as exc:
            print(f"{Fore.RED}[!] Cannot read wordlist: {exc}{Style.RESET_ALL}")
            return 1

    print(
        f"\n{Fore.YELLOW}[+] Enumerating subdomains "
        f"(concurrency={cfg.max_concurrency}, timeout={cfg.timeout_seconds}s)...{Style.RESET_ALL}"
    )
    report = enumerate_subdomains(domain, cfg, on_found=print_found)

    print(
        f"\n{Fore.CYAN}[*] Wordlist:{Style.RESET_ALL} "
        f"{report.wordlist_valid_entries} valid, "
        f"{report.wordlist_skipped_entries} skipped (blank/comment/invalid/duplicate)"
    )
    print(f"{Fore.CYAN}[*] Checked:{Style.RESET_ALL} {report.subdomains_checked}")
    print(f"{Fore.CYAN}[*] Found:{Style.RESET_ALL}   {len(report.results)}")
    print(f"{Fore.CYAN}[*] Errors:{Style.RESET_ALL}  {report.errors}")
    print(f"{Fore.CYAN}[*] Elapsed:{Style.RESET_ALL} {report.elapsed_seconds:.2f}s")

    if cfg.output_format != "none":
        out_path = export(report, cfg.output_format, cfg.output_path)
        if out_path:
            print(f"\n{Fore.GREEN}[+] Report written to {out_path}{Style.RESET_ALL}")

    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME.lower(),
        description="Uncover the real origin IP of a domain hidden behind a CDN.",
    )
    parser.add_argument("domain", help="Target domain or URL, e.g. example.com")
    parser.add_argument(
        "-w", "--wordlist", type=Path, default=DEFAULT_WORDLIST,
        help=f"Path to subdomain wordlist (default: {DEFAULT_WORDLIST.name})",
    )
    parser.add_argument(
        "-c", "--concurrency", type=int, default=40,
        help="Max concurrent subdomain probes (default: 40). Kept modest by "
             "default to avoid tripping WAF rate limits or looking like a flood.",
    )
    parser.add_argument("-t", "--timeout", type=float, default=8.0, help="Per-request timeout in seconds")
    parser.add_argument(
        "-f", "--format", choices=["csv", "none"], default="none",
        help="Output report format (default: none)",
    )
    parser.add_argument("-o", "--output", help="CSV output path (optional)")
    parser.add_argument("--skip-historical", action="store_true", help="Skip ViewDNS/SecurityTrails lookups")
    parser.add_argument("--skip-subdomains", action="store_true", help="Skip subdomain enumeration")
    parser.add_argument("--update-wordlist", action="store_true", help="Force-refresh the wordlist and exit")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompts")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    return parser


def main(argv: list[str] | None = None) -> int:
    colorama_init()
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    if args.update_wordlist:
        update_wordlist(args.wordlist)
        return 0

    domain = normalize_domain(args.domain)
    cfg = ScanConfig(
        timeout_seconds=args.timeout,
        max_concurrency=args.concurrency,
        output_format=args.format,
        output_path=args.output,
        wordlist_path=args.wordlist,
    )

    try:
        return run(domain, cfg, args)
    except (FileNotFoundError, ValueError) as exc:
        print(f"{Fore.RED}[!] {exc}{Style.RESET_ALL}")
        return 1
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Interrupted.{Style.RESET_ALL}")
        return 130


if __name__ == "__main__":
    sys.exit(main())
