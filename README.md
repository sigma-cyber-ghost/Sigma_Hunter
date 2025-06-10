# Sigma_Hunter
# AdminFinderPro - Advanced Admin Panel Discovery Tool

Websiter Admin Url founder is a powerful Python tool designed to discover hidden admin panels, login pages, and other administrative interfaces on websites. It employs multiple discovery techniques including path brute-forcing, robots.txt analysis, sitemap extraction, JavaScript analysis, and more.

## Features

- 🕵️‍♂️ CMS detection (WordPress, Joomla, Drupal, etc.)
- 🔍 Multiple discovery techniques:
  - Path brute-forcing with custom wordlists
  - Robots.txt analysis
  - Sitemap.xml extraction
  - JavaScript file analysis
  - Header analysis
  - HTML content scanning
- ⚡ Multi-threaded scanning
- 🎨 Color-coded console output
- 💾 CSV export for results
- 🔧 Comprehensive scan mode

## Installation

1. Clone the repository:
```bash
git clone 
cd 

pip3 install -r requirements.txt

pip3 install requests beautifulsoup4 colorama

python3 sigma_hunter.py https://example.com or example.com

python3 sigma_hunter.py https://example.com --full -t 50 -T 10 -o results.csv -w wordlists/custom.txt

  url                    Target URL to scan
  -o, --output OUTPUT    Output file to save results (CSV format)
  -t, --threads THREADS  Number of threads (default: 20)
  -T, --timeout TIMEOUT  Timeout in seconds (default: 5)
  -w, --wordlist WORDLIST
                         Custom wordlist file
  -f, --full             Enable comprehensive scan
---
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create a new branch (git checkout -b feature/your-feature)

Commit your changes (git commit -am 'Add some feature')

Push to the branch (git push origin feature/your-feature)

Create a new Pull Request
Disclaimer
This tool is intended for security research and unauthorized penetration testing only. Always use it on websites without explicit permission. The developers are not responsible for any misuse of this tool.
