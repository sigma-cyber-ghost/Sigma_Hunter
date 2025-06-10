import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import argparse
import os
import re
import json
import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import threading
import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

BANNER = rf"""{Fore.MAGENTA}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀Sigma_Cyber_Ghost⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀*Me 💀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⣤⣤⣄⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣴⣿⣿⣿⣿⣿⣿⣦⠀⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣾⣿⣿⠟⣻⣿⣿⡟⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣼⣿⣿⣿⣿⣼⡻⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣌⢻⣿⣿⣿⣿⣿⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣿⣦⣙⢿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Admin Webiste⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣿⣿⣿⣦⡙⢿⣿⣿⣿⣿⣿⣤⣀⠀⠀⠠⣶⡶⣶⣶⣶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⢿⣿⣿⣿⣿⣿⣿⣿⣦⡙⢿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣯⣿⣿⣶⣴⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠉⠉⣿⣯⣝⣋⡛⠟⠿⠿⠿⠿⠿⣿⡿⠿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢃⣤⣴⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⢿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⡄⠀⠈⠛⠿⠿⠿⠿⠟⠋⠁⢐⣿⣿⣟⣻⣿⣟⢿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⣿⣿⣿⣷⣬⣍⣛⣛⠿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⣘⣿⣿⣿⣿⣿⣿⣎⢿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣭⣿⣷⡀⠀⠀⠀⠀⠀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣩⣿⣿⣿⣿⣿⣿⣷⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣻⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⣦⣭⣝⡛⠿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣷⣶⣾⣿⡍⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⡿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠀
{Style.RESET_ALL}"""

# Extended paths across multiple categories
admin_paths = {
    "Admin Panel": [
        "admin", "administrator", "admin1", "admin2", "adminpanel", "admin_area", "webadmin", "cms/admin",
        "admin/login", "admin.php", "panel/admin", "wp-admin", "wp-login", "backend", "console", "control",
        "controlpanel", "dashboard", "directadmin", "direct-admin", "manage", "management", "manager", "monitor",
        "superadmin", "supervisor", "sysadmin", "system", "useradmin", "webmaster", "root", "secret", "private"
    ],
    "Login Pages": [
        "login", "signin", "auth", "user/login", "wp-login.php", "login.php", "login/admin", "member/login",
        "account/login", "signin.php", "auth.php", "authentication", "authenticate", "auth/login", "secure",
        "security", "oauth", "oauth2", "sso", "logon", "signon", "access", "portal"
    ],
    "Control Panels": [
        "cpanel", "controlpanel", "server/cpanel", "cpanel/login", "whm", "plesk", "webmin", "virtualmin",
        "vpanel", "ispconfig", "hestia", "zpanel", "centmin", "kloxo", "directadmin", "vestacp", "cyberpanel",
        "ehcp", "ajenti", "sentora", "froxlor", "interworx", "rcp", "rc", "admincp", "admin-cp", "control-panel"
    ],
    "User Portals": [
        "user", "users", "account", "dashboard", "profile", "userpanel", "portal", "client", "clientarea",
        "myaccount", "member", "members", "account-manager", "user-center", "user-home", "user-dashboard",
        "user-profile", "user-settings", "user-account", "member-area", "client-portal", "customer-portal",
        "user-portal", "account-portal", "profile.php", "account.php", "dashboard.php", "portal.php"
    ],
    "Database Interfaces": [
        "phpmyadmin", "pma", "adminer", "mysql-admin", "dbadmin", "database-admin", "dba", "db", "sqladmin",
        "sql-admin", "phpMyAdmin", "admin/mysql", "admin/db", "admin/database", "admin/phpmyadmin"
    ],
    "Development Tools": [
        "phpinfo", "info.php", "test.php", "debug", "status", "web-console", "console", "api/console",
        "api/doc", "swagger", "swagger-ui", "redoc", "api-docs", "graphql", "graphiql", "voyager",
        "admin/api", "admin/docs", "admin/console", "admin/tools", "admin/phpinfo"
    ],
    "Backup Files": [
        "backup", "backups", "bak", "back", "old", "archive", "backup.zip", "backup.tar", "backup.tar.gz",
        "backup.sql", "db.sql", "database.sql", "dump.sql", "site.bak", "website.bak", "config.bak",
        "config.old", "config.php.bak", "wp-config.php.bak", ".git", ".svn", ".env", ".env.bak"
    ]
}

# Global variables
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
found_count = 0
lock = threading.Lock()
cms_type = "Unknown"
wordlist = []

# Load custom wordlist if available
def load_wordlist(wordlist_file):
    global wordlist
    if wordlist_file and os.path.exists(wordlist_file):
        try:
            with open(wordlist_file, 'r') as f:
                wordlist = [line.strip() for line in f.readlines() if line.strip()]
            print(f"{Fore.CYAN}[+] Loaded {len(wordlist)} paths from custom wordlist{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error loading wordlist: {e}{Style.RESET_ALL}")
    else:
        # Generate wordlist from admin_paths
        for category, paths in admin_paths.items():
            wordlist.extend(paths)
        # Remove duplicates
        wordlist = list(set(wordlist))
        print(f"{Fore.CYAN}[+] Using built-in wordlist with {len(wordlist)} paths{Style.RESET_ALL}")

# Detect CMS
def detect_cms(url):
    global cms_type
    try:
        response = session.get(url, timeout=5)
        content = response.text.lower()
        headers = response.headers

        # Check headers
        if 'x-powered-by' in headers:
            if 'wordpress' in headers['x-powered-by'].lower():
                cms_type = "WordPress"
                return
            elif 'joomla' in headers['x-powered-by'].lower():
                cms_type = "Joomla"
                return

        # Check content patterns
        if 'wp-content' in content or 'wp-includes' in content or 'wordpress' in content:
            cms_type = "WordPress"
        elif 'joomla' in content or 'Joomla!' in content:
            cms_type = "Joomla"
        elif 'drupal' in content:
            cms_type = "Drupal"
        elif '/skin/frontend' in content or '/js/mage' in content:
            cms_type = "Magento"
        elif 'content="Sitefinity' in content:
            cms_type = "Sitefinity"
        elif '/umbraco/' in content or 'umbraco' in content:
            cms_type = "Umbraco"
        elif 'squarespace' in content or 'static.squarespace.com' in content:
            cms_type = "Squarespace"
        elif 'shopify' in content:
            cms_type = "Shopify"
        elif 'wix' in content:
            cms_type = "Wix"
        else:
            cms_type = "Unknown"
    except:
        cms_type = "Unknown"

# Check robots.txt
def check_robots(url):
    try:
        robots_url = urljoin(url, '/robots.txt')
        response = session.get(robots_url, timeout=5)
        if response.status_code == 200:
            paths = []
            for line in response.text.split('\n'):
                if line.startswith('Disallow:'):
                    path = line.split(': ')[1].strip()
                    paths.append(path)
            return paths
    except:
        return []

# Check sitemap.xml
def check_sitemap(url):
    try:
        sitemap_url = urljoin(url, '/sitemap.xml')
        response = session.get(sitemap_url, timeout=5)
        if response.status_code == 200:
            paths = []
            soup = BeautifulSoup(response.text, 'lxml')
            for loc in soup.find_all('loc'):
                path = urlparse(loc.text).path
                if path:
                    paths.append(path)
            return paths
    except:
        return []

# Analyze JavaScript files
def analyze_js(url):
    try:
        response = session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        js_paths = []
        
        # Find all script tags
        for script in soup.find_all('script'):
            if script.has_attr('src'):
                js_url = script['src']
                if not js_url.startswith(('http', '//')):
                    js_url = urljoin(url, js_url)
                try:
                    js_response = session.get(js_url, timeout=5)
                    if js_response.status_code == 200:
                        # Look for admin paths in JS content
                        js_content = js_response.text
                        for path in wordlist:
                            if f'"{path}"' in js_content or f"'{path}'" in js_content:
                                js_paths.append(f"/{path}")
                except:
                    continue
        return js_paths
    except:
        return []

# Check common backup files
def check_backups(url):
    backups = []
    backup_extensions = ['.bak', '.old', '.backup', '.copy', '.orig', '.save', '.swp', '.tmp']
    backup_files = [
        'config', 'configuration', 'settings', 'db', 'database', 'backup', 
        'website', 'site', 'app', 'application', 'index', 'index.php', 'index.html',
        'wp-config', 'wp-config.php', 'wp-config.php.bak', '.env', 'htaccess'
    ]
    
    for file in backup_files:
        for ext in backup_extensions:
            backups.append(f"{file}{ext}")
    
    return backups

# Check for admin headers
def check_admin_headers(url):
    try:
        response = session.head(url, timeout=5)
        headers = response.headers
        
        admin_headers = [
            'x-admin', 'admin', 'admin-path', 'admin-portal', 'admin-url',
            'x-backend', 'backend', 'x-dashboard', 'dashboard', 'x-login', 
            'x-secret', 'x-admin-url', 'x-control-panel'
        ]
        
        found_headers = []
        for header in admin_headers:
            if header in headers:
                found_headers.append(f"{header}: {headers[header]}")
        
        return found_headers
    except:
        return []

# Analyze HTML content for admin patterns
def analyze_html(url):
    try:
        response = session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for common admin keywords in content
        admin_keywords = [
            'admin', 'administrator', 'login', 'sign in', 'control panel',
            'dashboard', 'backend', 'cpanel', 'user portal', 'manage',
            'administration', 'admin area', 'admin console'
        ]
        
        found_patterns = []
        text = soup.get_text().lower()
        for keyword in admin_keywords:
            if keyword in text:
                found_patterns.append(f"Content contains '{keyword}'")
        
        # Look for login forms
        login_forms = soup.find_all('form', {'action': True})
        for form in login_forms:
            if 'login' in form.get('action', '').lower() or 'signin' in form.get('action', '').lower():
                found_patterns.append(f"Login form found at {form['action']}")
        
        return found_patterns
    except:
        return []

# Check a single URL
def check_url(base_url, path, output_file, timeout):
    global found_count
    url = urljoin(base_url, path)
    
    try:
        response = session.head(url, timeout=timeout, allow_redirects=False)
        status = response.status_code
        
        # Skip 404s
        if status == 404:
            return None
        
        # Follow redirects for 3xx responses
        if 300 <= status < 400:
            redirect_url = response.headers.get('Location', '')
            if redirect_url:
                # Handle relative redirects
                if not redirect_url.startswith('http'):
                    redirect_url = urljoin(url, redirect_url)
                try:
                    redirect_response = session.head(redirect_url, timeout=timeout)
                    status = redirect_response.status_code
                    url = redirect_url
                except:
                    return None
        
        # Get final URL after redirects
        final_url = url
        
        # Get page title if it's a 200 response
        title = ""
        if status == 200:
            try:
                response = session.get(url, timeout=timeout)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string.strip() if soup.title else "No title"
            except:
                title = "Title unavailable"
        
        result = {
            "url": final_url,
            "status": status,
            "title": title,
            "path": path
        }
        
        with lock:
            found_count += 1
            status_color = Fore.GREEN if status == 200 else Fore.YELLOW
            print(f"{status_color}[{status}] {final_url} {Fore.CYAN}{title}{Style.RESET_ALL}")
            
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(f"{status},{final_url},{title}\n")
        
        return result
    except requests.exceptions.RequestException:
        return None
    except Exception as e:
        print(f"{Fore.RED}[!] Error checking {url}: {e}{Style.RESET_ALL}")
        return None

# Main scanning function
def scan(url, output_file=None, threads=20, timeout=5, full_scan=False):
    global found_count
    found_count = 0
    start_time = time.time()
    
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    url = url.rstrip("/")
    print(f"\n{Fore.YELLOW}[+] Scanning {url}{Style.RESET_ALL}")
    
    # CMS detection
    detect_cms(url)
    print(f"{Fore.CYAN}[*] CMS Detected: {cms_type}{Style.RESET_ALL}")
    
    # Initialize scanning paths
    scan_paths = []
    
    # Add wordlist paths
    scan_paths.extend(wordlist)
    
    # Add CMS-specific paths
    if cms_type == "WordPress":
        scan_paths.extend(["wp-admin", "wp-login.php", "login", "admin"])
    elif cms_type == "Joomla":
        scan_paths.extend(["administrator", "admin"])
    elif cms_type == "Drupal":
        scan_paths.extend(["user/login", "admin"])
    
    # Full scan features
    if full_scan:
        print(f"{Fore.CYAN}[*] Performing comprehensive scan{Style.RESET_ALL}")
        
        # Robots.txt analysis
        print(f"{Fore.BLUE}[*] Checking robots.txt...{Style.RESET_ALL}")
        robot_paths = check_robots(url)
        if robot_paths:
            print(f"{Fore.GREEN}[+] Found {len(robot_paths)} paths in robots.txt{Style.RESET_ALL}")
            scan_paths.extend(robot_paths)
        
        # Sitemap.xml analysis
        print(f"{Fore.BLUE}[*] Checking sitemap.xml...{Style.RESET_ALL}")
        sitemap_paths = check_sitemap(url)
        if sitemap_paths:
            print(f"{Fore.GREEN}[+] Found {len(sitemap_paths)} paths in sitemap.xml{Style.RESET_ALL}")
            scan_paths.extend(sitemap_paths)
        
        # JavaScript analysis
        print(f"{Fore.BLUE}[*] Analyzing JavaScript files...{Style.RESET_ALL}")
        js_paths = analyze_js(url)
        if js_paths:
            print(f"{Fore.GREEN}[+] Found {len(js_paths)} potential paths in JS files{Style.RESET_ALL}")
            scan_paths.extend(js_paths)
        
        # Backup files
        print(f"{Fore.BLUE}[*] Checking common backup files...{Style.RESET_ALL}")
        backup_files = check_backups(url)
        scan_paths.extend(backup_files)
        
        # Header analysis
        print(f"{Fore.BLUE}[*] Analyzing headers...{Style.RESET_ALL}")
        admin_headers = check_admin_headers(url)
        if admin_headers:
            print(f"{Fore.GREEN}[+] Found admin-related headers:{Style.RESET_ALL}")
            for header in admin_headers:
                print(f"  {Fore.CYAN}{header}{Style.RESET_ALL}")
        
        # HTML analysis
        print(f"{Fore.BLUE}[*] Analyzing page content...{Style.RESET_ALL}")
        html_patterns = analyze_html(url)
        if html_patterns:
            print(f"{Fore.GREEN}[+] Found admin patterns in HTML:{Style.RESET_ALL}")
            for pattern in html_patterns:
                print(f"  {Fore.CYAN}{pattern}{Style.RESET_ALL}")
    
    # Remove duplicates
    scan_paths = list(set(scan_paths))
    print(f"{Fore.CYAN}[*] Testing {len(scan_paths)} unique paths with {threads} threads{Style.RESET_ALL}")
    
    # Create output file if specified
    if output_file:
        with open(output_file, 'w') as f:
            f.write("Status,URL,Title\n")
    
    # Threaded scanning
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_url, url, path, output_file, timeout): path for path in scan_paths}
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    # Print summary
    elapsed_time = time.time() - start_time
    print(f"\n{Fore.GREEN}[+] Scan completed in {elapsed_time:.2f} seconds{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Found {found_count} potential admin interfaces{Style.RESET_ALL}")
    
    if output_file:
        print(f"{Fore.GREEN}[+] Results saved to {output_file}{Style.RESET_ALL}")
    
    return results

# Main function
def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="Advanced Admin Panel Finder Tool")
    parser.add_argument("url", nargs="?", help="Target URL to scan")
    parser.add_argument("-o", "--output", help="Output file to save results (CSV format)")
    parser.add_argument("-t", "--threads", type=int, default=20, 
                        help="Number of threads (default: 20)")
    parser.add_argument("-T", "--timeout", type=int, default=5, 
                        help="Timeout in seconds (default: 5)")
    parser.add_argument("-w", "--wordlist", help="Custom wordlist file")
    parser.add_argument("-f", "--full", action="store_true", 
                        help="Enable comprehensive scan (robots.txt, sitemap, JS analysis, etc.)")
    
    args = parser.parse_args()
    
    if not args.url:
        parser.print_help()
        sys.exit(1)
    
    # Load wordlist
    load_wordlist(args.wordlist)
    
    # Start scanning
    scan(args.url, args.output, args.threads, args.timeout, args.full)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
