DELTA BLACK

██████╗ ███████╗██╗  ████████╗ █████╗
██╔══██╗██╔════╝██║  ╚══██╔══╝██╔══██╗
██║  ██║█████╗  ██║     ██║   ███████║
██║  ██║██╔══╝  ██║     ██║   ██╔══██║
██████╔╝███████╗███████╗██║   ██║  ██║
╚═════╝ ╚══════╝╚══════╝╚═╝   ╚═╝  ╚═╝

        B L A C K   R E C O N   S U I T E

<p align="center">
  <img src="assets/delta-black.svg" alt="DELTA BLACK" width="720">
</p><p align="center">
  <b>CDN / DNS Exposure Assessment Toolkit</b><br>
  Focused, modular, terminal-first reconnaissance for authorized security testing.
</p><p align="center">
  <a href="https://github.com/DELTAxBLACK/DELTAx80BLACK">GitHub</a> •
  <a href="https://t.me/Delta167">Telegram</a> •
  <a href="LICENSE">MIT License</a>
</p>---

Overview

DELTA BLACK is a terminal-first reconnaissance toolkit designed for authorized security assessments.

It focuses on identifying DNS and CDN-related exposure and gathering publicly available information about a target domain.

The toolkit can perform:

- Cloudflare detection
- Historical DNS/IP lookups
- Subdomain enumeration
- DNS resolution
- HTTP server/header inspection
- TLS certificate inspection
- Configurable concurrency
- Configurable request timeouts
- Optional CSV reporting
- Built-in wordlists
- Clean terminal output

«Authorization required: Only use DELTA BLACK against systems you own or systems for which you have explicit permission to perform security testing.»

---

Features

- [x] Cloudflare detection
- [x] Historical IP lookups
- [x] Subdomain enumeration
- [x] DNS resolution
- [x] HTTP header inspection
- [x] TLS certificate inspection
- [x] Configurable concurrency
- [x] Configurable timeout
- [x] Custom wordlists
- [x] Optional CSV output
- [x] Verbose logging
- [x] Interactive confirmation
- [x] Optional SecurityTrails integration
- [x] Termux support
- [x] Kali Linux support
- [x] Debian / Ubuntu support
- [x] Windows support
- [x] macOS support

---

Requirements

DELTA BLACK requires:

- Python 3.9+
- Git
- pip
- Internet connection
- Python dependencies listed in "requirements.txt"

Recommended:

- Python virtual environment
- Updated system packages
- A dedicated authorized testing environment

---

Installation

Kali Linux

Update your package lists:

sudo apt update

Install the required packages:

sudo apt install -y git python3 python3-pip python3-venv

Clone DELTA BLACK:

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git

Enter the project directory:

cd DELTAx80BLACK

Create a virtual environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Install Python dependencies:

python3 -m pip install -r requirements.txt

Run the program:

python3 delta_black.py example.com

Kali — Quick Installation

sudo apt update && sudo apt install -y git python3 python3-pip python3-venv && git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git && cd DELTAx80BLACK && python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -r requirements.txt

---

Debian / Ubuntu

Update the system:

sudo apt update

Install Python and Git:

sudo apt install -y git python3 python3-pip python3-venv

Clone the repository:

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git

Enter the directory:

cd DELTAx80BLACK

Create a virtual environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Install dependencies:

python3 -m pip install -r requirements.txt

Run:

python3 delta_black.py example.com

---

Termux / Android

DELTA BLACK can also be used in Termux.

Update Termux packages:

pkg update
pkg upgrade

Install Git and Python:

pkg install git python

Clone the repository:

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git

Enter the project:

cd DELTAx80BLACK

Install Python dependencies:

python -m pip install -r requirements.txt

Run:

python delta_black.py example.com

Termux — Quick Installation

pkg update && pkg install -y git python && git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git && cd DELTAx80BLACK && python -m pip install -r requirements.txt

«Termux note: Some Python packages may require additional build dependencies depending on the Android/Termux environment. If a dependency fails to install, check the package's error message and install the required Termux package.»

---

Windows

Install:

- Python 3
- Git

Then open PowerShell or Command Prompt.

Clone the repository:

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git

Enter the directory:

cd DELTAx80BLACK

Create a virtual environment:

python -m venv .venv

Activate it:

.venv\Scripts\activate

Install dependencies:

python -m pip install -r requirements.txt

Run:

python delta_black.py example.com

---

macOS

Install Git and Python 3.

Clone the repository:

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git

Enter the project:

cd DELTAx80BLACK

Create a virtual environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Install dependencies:

python3 -m pip install -r requirements.txt

Run:

python3 delta_black.py example.com

---

Quick Start

After installation, run:

python3 delta_black.py example.com

Replace "example.com" with a domain you are authorized to assess.

For Termux:

python delta_black.py example.com

---

Usage

Basic Scan

python3 delta_black.py example.com

---

Skip Historical Lookups

python3 delta_black.py example.com --skip-historical

---

Skip Subdomain Enumeration

python3 delta_black.py example.com --skip-subdomains

---

Custom Wordlist

python3 delta_black.py example.com --wordlist wordlist.txt

---

Configure Concurrency

python3 delta_black.py example.com --concurrency 20

---

Configure Timeout

python3 delta_black.py example.com --timeout 10

---

Concurrency + Timeout

python3 delta_black.py example.com --concurrency 20 --timeout 10

---

CSV Report

Export results to CSV:

python3 delta_black.py example.com --format csv --output results.csv

---

Skip Interactive Confirmation

python3 delta_black.py example.com --yes

---

Verbose Mode

python3 delta_black.py example.com --verbose

---

Update Wordlist

python3 delta_black.py example.com --update-wordlist

---

Show Help

python3 delta_black.py -h

---

Command Reference

Option| Description
"--skip-historical"| Skip historical DNS/IP lookups
"--skip-subdomains"| Skip subdomain enumeration
"--wordlist"| Specify a custom wordlist
"--concurrency"| Configure concurrent workers
"--timeout"| Configure network timeout
"--format csv"| Enable CSV reporting
"--output"| Specify output file
"--yes"| Skip interactive confirmation
"--verbose"| Enable verbose logging
"--update-wordlist"| Refresh the bundled wordlist
"-h"| Display help

---

Configuration

DELTA BLACK supports optional configuration through:

config.ini

Example:

[DEFAULT]
securitytrails_api_key = your_key_here

SecurityTrails

SecurityTrails integration is optional.

If you have an authorized API key, add it to "config.ini".

Never commit real API keys to GitHub.

Recommended practice:

config.ini

should not contain real credentials when the repository is public.

---

Project Structure

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

Testing

Run the test suite from the project directory:

python3 -m unittest discover -s tests -v

On Termux:

python -m unittest discover -s tests -v

---

Troubleshooting

Python Not Found

Check Python:

python3 --version

or:

python --version

---

pip Not Found

Kali / Debian / Ubuntu:

sudo apt install python3-pip

Termux:

pkg install python

---

Git Not Found

Kali / Debian / Ubuntu:

sudo apt install git

Termux:

pkg install git

---

Permission Problems on Linux

Avoid installing Python packages globally when possible.

Create a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Then:

python3 -m pip install -r requirements.txt

---

Updating DELTA BLACK

Enter the project directory:

cd DELTAx80BLACK

Pull the latest version:

git pull

Update dependencies:

python3 -m pip install -r requirements.txt --upgrade

---

Uninstall

Remove the project directory:

cd ..
rm -rf DELTAx80BLACK

If you created a virtual environment, it is removed together with the project directory.

---

Output

By default, DELTA BLACK displays results directly in the terminal.

CSV output is optional:

python3 delta_black.py example.com --format csv --output results.csv

DELTA BLACK does not generate JSON report files.

---

Wordlists

The project includes bundled wordlists:

wordlist.txt
wordlist2.txt

You can specify another authorized wordlist:

python3 delta_black.py example.com --wordlist my-wordlist.txt

---

Recommended Workflow

For an authorized assessment:

git clone https://github.com/DELTAxBLACK/DELTAx80BLACK.git
cd DELTAx80BLACK
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 delta_black.py example.com

For a faster scan without historical lookups:

python3 delta_black.py example.com --skip-historical

For CSV reporting:

python3 delta_black.py example.com --format csv --output results.csv

---

Supported Platforms

Platform| Status
Kali Linux| Supported
Debian| Supported
Ubuntu| Supported
Termux / Android| Supported
Windows| Supported
macOS| Supported

---

Security & Privacy

DELTA BLACK is intended for authorized reconnaissance and security assessment.

Do not use the toolkit to:

- Access systems without permission
- Attempt unauthorized intrusion
- Disrupt services
- Circumvent security controls
- Collect private information without authorization

Always follow the rules of engagement defined by the system owner.

---

Legal Notice

DELTA BLACK is provided for authorized security testing and educational purposes.

You are responsible for ensuring that you have appropriate authorization before scanning a target.

The developers and contributors are not responsible for misuse, unauthorized scanning, damage, disruption, or unlawful activity resulting from use of this project.

---

Attribution

<p align="center">
  <a href="https://t.me/Delta167">
    <img src="https://img.shields.io/badge/Telegram-%40Delta167-111827?style=for-the-badge&logo=telegram&logoColor=38BDF8" alt="Telegram">
  </a>
</p>The original MIT license and copyright notice are preserved in "LICENSE".

Upstream credit remains intact.

---

Modified By

DELTA

Telegram: @Delta167

---

License

This project is licensed under the MIT License.

See:

LICENSE

for the complete license text.

---

<p align="center">DELTA BLACK

"BLACK RECON SUITE"

CDN / DNS Exposure Assessment Toolkit

</p>
