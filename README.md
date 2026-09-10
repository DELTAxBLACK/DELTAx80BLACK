# DELTA BLACK

```text
██████╗ ███████╗██╗  ████████╗ █████╗
██╔══██╗██╔════╝██║  ╚══██╔══╝██╔══██╗
██║  ██║█████╗  ██║     ██║   ███████║
██║  ██║██╔══╝  ██║     ██║   ██╔══██║
██████╔╝███████╗███████╗██║   ██║  ██║
╚═════╝ ╚══════╝╚══════╝╚═╝   ╚═╝  ╚═╝

        B L A C K   R E C O N   S U I T E
```

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/235224431-e8c8c12e-6826-47f1-89fb-2ddad83b3abf.gif" width="450">
</p>

<p align="center">
  <img src="assets/delta-black.svg" alt="DELTA BLACK" width="720">
</p>

<p align="center">
  <b>CDN / DNS exposure assessment toolkit</b><br>
  Focused, modular, terminal-first reconnaissance for authorized testing.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Termux%20%7C%20Kali-111827?style=for-the-badge&logo=linux&logoColor=38BDF8">
  <img src="https://img.shields.io/badge/python-3.8%2B-111827?style=for-the-badge&logo=python&logoColor=38BDF8">
  <img src="https://img.shields.io/badge/license-MIT-111827?style=for-the-badge">
</p>

<p align="center">
  <a href="https://t.me/Delta167">Telegram</a> •
  <a href="LICENSE">MIT License</a>
</p>

---

## Overview

DELTA BLACK checks a target domain for Cloudflare presence, inspects historical DNS sources, and enumerates common subdomains that may expose infrastructure outside a CDN.

The project is intended for systems you own or have explicit permission to assess.

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/229223263-cf2e4b07-2615-4f87-9c38-e37600f8381a.gif" width="380">
</p>

## Highlights

- Cloudflare detection
- Historical IP lookups
- Concurrent subdomain enumeration
- DNS resolution
- Web server header detection
- TLS certificate inspection
- Configurable concurrency and timeouts
- Optional CSV reporting
- Clean terminal output
- Built-in wordlist handling
- No JSON report generation or JSON output files

## Project Layout

```text
DELTA-BLACK/
├── assets/
│   └── delta-black.svg
├── tests/
│   ├── __init__.py
│   ├── test_historical.py
│   └── test_scanner.py
├── config.ini
├── config.py
├── delta_black.py
├── historical.py
├── network.py
├── report.py
├── requirements.txt
├── scanner.py
├── wordlist.txt
├── wordlist2.txt
├── LICENSE
└── README.md
```

## Installation

### Kali Linux

```bash
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git
cd DELTAx80BLACK
pip3 install -r requirements.txt
python3 delta_black.py -h
```

### Termux

```bash
pkg update && pkg upgrade -y
pkg install -y python git
git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git
cd DELTAx80BLACK
pip install -r requirements.txt
python delta_black.py -h
```

## Usage

Basic scan:

```bash
python3 delta_black.py example.com
```

Run without historical lookups:

```bash
python3 delta_black.py example.com --skip-historical
```

Run without subdomain enumeration:

```bash
python3 delta_black.py example.com --skip-subdomains
```

Use a custom wordlist:

```bash
python3 delta_black.py example.com --wordlist wordlist.txt
```

Adjust concurrency and timeout:

```bash
python3 delta_black.py example.com --concurrency 20 --timeout 10
```

Write an optional CSV report:

```bash
python3 delta_black.py example.com --format csv --output results.csv
```

Skip interactive confirmation:

```bash
python3 delta_black.py example.com --yes
```

Enable verbose logging:

```bash
python3 delta_black.py example.com --verbose
```

Refresh the bundled wordlist:

```bash
python3 delta_black.py example.com --update-wordlist
```

Show all command-line options:

```bash
python3 delta_black.py -h
```

## SecurityTrails

SecurityTrails support is optional.

Set the API key in `config.ini`:

```ini
[DEFAULT]
securitytrails_api_key = your_key_here
```

Do not commit real API keys to a public repository.

## Output

DELTA BLACK does not generate JSON files.

By default, scan results are printed directly to the terminal. CSV export is available only when explicitly requested with `--format csv`.

## Development

Run the test suite from the project directory:

```bash
python3 -m unittest discover -s tests -v
```

---

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212284087-bbe7e430-757e-4901-90bf-4cd2ce3e1852.gif" width="420">
</p>

## Attribution

[![Contact](https://img.shields.io/badge/Telegram-%40Delta167-111827?style=for-the-badge&logo=telegram&logoColor=38BDF8)](https://t.me/Delta167)

The original MIT license and copyright notice are preserved in `LICENSE`.
Upstream credit remains intact.

## Modified By

**DELTA**

Telegram: **@Delta167**

## Legal Notice

Use DELTA BLACK only against systems you own or systems for which you have explicit authorization to perform security testing.

---
