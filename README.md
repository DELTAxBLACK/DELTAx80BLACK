
DELTA BLACK

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/235224431-e8c8c12e-6826-47f1-89fb-2ddad83b3abf.gif" width="700">
</p>██████╗ ███████╗██╗  ████████╗ █████╗
██╔══██╗██╔════╝██║  ╚══██╔══╝██╔══██╗
██║  ██║█████╗  ██║     ██║   ███████║
██║  ██║██╔══╝  ██║     ██╔══██╗
██████╔╝███████╗███████╗██║   ██║  ██║
╚═════╝ ╚══════╝╚══════╝╚═╝   ╚═╝  ╚═╝

        B L A C K   R E C O N   S U I T E

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/229223263-cf2e4b07-2615-4f87-9c38-e37600f8381a.gif" width="500">
</p><p align="center">
  <b>CDN / DNS EXPOSURE ASSESSMENT TOOLKIT</b><br>
  Focused • Modular • Terminal-First • Authorized Security Testing
</p><p align="center">""Python" (https://img.shields.io/badge/Python-3.9%2B-111827?style=for-the-badge&logo=python&logoColor=38BDF8)" (https://www.python.org/)
""Platform" (https://img.shields.io/badge/Platform-Kali%20%7C%20Linux%20%7C%20Termux-111827?style=for-the-badge&logo=linux&logoColor=white)" (https://github.com/DELTAxBLACK/DELTAx80BLACK)
""License" (https://img.shields.io/badge/License-MIT-111827?style=for-the-badge)" (LICENSE)

</p><p align="center">
  <a href="https://github.com/DELTAxBLACK/DELTAx80BLACK">GitHub</a> •
  <a href="https://t.me/Delta167">Telegram</a>
</p>---

"01" — OVERVIEW

DELTA BLACK is a terminal-first reconnaissance toolkit for authorized security assessments.

It focuses on DNS, CDN, subdomain and publicly available network information that can help identify infrastructure exposure.

«AUTHORIZED TESTING ONLY

Use DELTA BLACK only against systems you own or systems for which you have explicit permission to perform security testing.»

---

"02" — FEATURES

[+] Cloudflare Detection
[+] Historical DNS / IP Lookups
[+] Subdomain Enumeration
[+] DNS Resolution
[+] HTTP Header Inspection
[+] TLS Certificate Inspection
[+] Configurable Concurrency
[+] Configurable Timeouts
[+] Custom Wordlists
[+] CSV Reporting
[+] Verbose Logging
[+] SecurityTrails Integration
[+] Kali Linux Support
[+] Termux / Android Support
[+] Linux Support
[+] Windows Support
[+] macOS Support

---

"03" — INSTALLATION

"KALI LINUX"

01 — Update system

sudo apt update
sudo apt upgrade -y

02 — Install requirements

sudo apt install -y git python3 python3-pip python3-venv

03 — Clone DELTA BLACK

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git

04 — Enter directory

cd DELTAx80BLACK

05 — Create virtual environment

python3 -m venv .venv

06 — Activate environment

source .venv/bin/activate

07 — Install Python dependencies

python3 -m pip install -r requirements.txt

08 — Start DELTA BLACK

python3 delta_black.py example.com

---

"KALI — QUICK INSTALL"

sudo apt update && \
sudo apt install -y git python3 python3-pip python3-venv && \
git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git && \
cd DELTAx80BLACK && \
python3 -m venv .venv && \
source .venv/bin/activate && \
python3 -m pip install -r requirements.txt

Run:

python3 delta_black.py example.com

---

"04" — TERMUX / ANDROID

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/235224431-e8c8c12e-6826-47f1-89fb-2ddad83b3abf.gif" width="450">
</p>01 — Update Termux

pkg update
pkg upgrade -y

02 — Install Git + Python

pkg install -y git python

03 — Clone repository

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git

04 — Enter project

cd DELTAx80BLACK

05 — Install dependencies

python -m pip install -r requirements.txt

06 — Run

python delta_black.py example.com

---

"TERMUX — QUICK INSTALL"

pkg update -y && \
pkg install -y git python && \
git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git && \
cd DELTAx80BLACK && \
python -m pip install -r requirements.txt

Run:

python delta_black.py example.com

---

"05" — DEBIAN / UBUNTU

sudo apt update
sudo apt install -y git python3 python3-pip python3-venv

Clone:

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git
cd DELTAx80BLACK

Create environment:

python3 -m venv .venv
source .venv/bin/activate

Install:

python3 -m pip install -r requirements.txt

Run:

python3 delta_black.py example.com

---

"06" — WINDOWS

Install Python 3 and Git first.

Clone:

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git

Enter directory:

cd DELTAx80BLACK

Create virtual environment:

python -m venv .venv

Activate:

.venv\Scripts\activate

Install dependencies:

python -m pip install -r requirements.txt

Run:

python delta_black.py example.com

---

"07" — macOS

Clone:

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git
cd DELTAx80BLACK

Create environment:

python3 -m venv .venv
source .venv/bin/activate

Install:

python3 -m pip install -r requirements.txt

Run:

python3 delta_black.py example.com

---

"08" — QUICK START

After installation:

python3 delta_black.py example.com

For Termux:

python delta_black.py example.com

Replace "example.com" with a domain you are authorized to assess.

---

"09" — USAGE

Basic scan

python3 delta_black.py example.com

Skip historical lookups

python3 delta_black.py example.com --skip-historical

Skip subdomain enumeration

python3 delta_black.py example.com --skip-subdomains

Custom wordlist

python3 delta_black.py example.com --wordlist wordlist.txt

Configure concurrency

python3 delta_black.py example.com --concurrency 20

Configure timeout

python3 delta_black.py example.com --timeout 10

CSV report

python3 delta_black.py example.com --format csv --output results.csv

Skip confirmation

python3 delta_black.py example.com --yes

Verbose mode

python3 delta_black.py example.com --verbose

Update wordlist

python3 delta_black.py example.com --update-wordlist

Show help

python3 delta_black.py -h

---

"10" — COMMAND OPTIONS

Option| Description
"--skip-historical"| Skip historical DNS/IP lookups
"--skip-subdomains"| Skip subdomain enumeration
"--wordlist"| Use a custom wordlist
"--concurrency"| Configure concurrent workers
"--timeout"| Configure network timeout
"--format csv"| Enable CSV output
"--output"| Specify report filename
"--yes"| Skip confirmation
"--verbose"| Enable verbose output
"--update-wordlist"| Refresh wordlist
"-h"| Show help

---

"11" — CONFIGURATION

Optional configuration is stored in:

config.ini

Example:

[DEFAULT]
securitytrails_api_key = your_key_here

SecurityTrails integration is optional.

Never commit real API keys or credentials to a public repository.

---

"12" — PROJECT STRUCTURE

DELTAx80BLACK/
│
├── assets/
│   └── delta-black.svg
│
├── tests/
│   ├── __init__.py
│   ├── test_historical.py
│   └── test_scanner.py
│
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

---

"13" — WORDLISTS

Bundled wordlists:

wordlist.txt
wordlist2.txt

Custom wordlist:

python3 delta_black.py example.com --wordlist my-wordlist.txt

---

"14" — TESTING

Run tests:

python3 -m unittest discover -s tests -v

Termux:

python -m unittest discover -s tests -v

---

"15" — UPDATE

Enter the repository:

cd DELTAx80BLACK

Pull the latest changes:

git pull

Update dependencies:

python3 -m pip install -r requirements.txt --upgrade

---

"16" — TROUBLESHOOTING

Check Python

python3 --version

or:

python --version

Check Git

git --version

Check pip

python3 -m pip --version

Reinstall dependencies

python3 -m pip install -r requirements.txt --upgrade

Linux virtual environment

python3 -m venv .venv
source .venv/bin/activate

---

"17" — OUTPUT

Results are displayed directly in the terminal by default.

Optional CSV output:

python3 delta_black.py example.com --format csv --output results.csv

DELTA BLACK does not generate JSON report files.

---

"18" — SUPPORTED PLATFORMS

┌──────────────────────────────┐
│        DELTA BLACK           │
├──────────────────────────────┤
│ ✓ Kali Linux                 │
│ ✓ Debian                     │
│ ✓ Ubuntu                     │
│ ✓ Termux / Android           │
│ ✓ Windows                    │
│ ✓ macOS                      │
└──────────────────────────────┘

---

"19" — SECURITY NOTICE

DELTA BLACK is intended for authorized security testing and educational environments.

Only scan systems where you have explicit authorization.

Do not use this project for unauthorized access, disruption, or testing against systems without permission.

---

"20" — ATTRIBUTION

<p align="center">
  <a href="https://t.me/Delta167">
    <img src="https://img.shields.io/badge/Telegram-%40Delta167-111827?style=for-the-badge&logo=telegram&logoColor=38BDF8" alt="Telegram">
  </a>
</p>The original MIT license and copyright notice are preserved in "LICENSE".

Upstream credit remains intact.

---

"21" — MODIFIED BY

██████╗ ███████╗██╗  ████████╗ █████╗
██╔══██╗██╔════╝██║  ╚══██╔══╝██╔══██╗
██║  ██║█████╗  ██║     ██║   ███████║
██║  ██║██╔══╝  ██║     ██║   ██╔══██║
██████╔╝███████╗███████╗██║   ██║  ██║
╚═════╝ ╚══════╝╚══════╝╚═╝   ╚═╝  ╚═╝

                 DELTA

Modified By: DELTA

Telegram: "@Delta167" (https://t.me/Delta167)

---

"22" — LICENSE

This project is licensed under the MIT License.

See ""LICENSE"" (LICENSE) for the complete license text.

---

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/229223263-cf2e4b07-2615-4f87-9c38-e37600f8381a.gif" width="450">
</p><p align="center">
  <b>DELTA BLACK</b><br>
  <code>BLACK RECON SUITE</code><br><br>
  <sub>Built for authorized security research.</sub>
</p>
