# 🏦 VulnBank

<div align="center">
  <h3>Intentionally Vulnerable Web Application for Security Training</h3>
  <p>A comprehensive, feature-rich banking application built with Django, packed with OWASP Top 10 vulnerabilities for penetration testers, security researchers, and developers.</p>
</div>

---

## 🌟 Overview
**VulnBank** is a simulated modern banking system that has been intentionally developed with weak security controls and vulnerable code. It provides a legal and completely safe environment to practice web exploitation techniques, test automated security scanners (like `AXON`), and understand secure coding practices by finding and fixing real-world vulnerabilities.

## 🎯 Intended Audience
- **Bug Bounty Hunters & Pentesters:** Hone your skills on realistic exploitation chains.
- **Cybersecurity Students:** Learn how OWASP Top 10 vulnerabilities manifest in a real codebase.
- **DevSecOps & Tool Developers:** Use this as a playground to benchmark automated vulnerability scanners.

---

## 🛑 Included Vulnerabilities (OWASP Top 10)

The platform is intentionally riddled with critical vulnerabilities:

| Vulnerability Type | Description & Location Hint |
|--------------------|-----------------------------|
| **SQL Injection (SQLi)** | Exists in the search functionalities, login bypass, and transaction history filters. |
| **Cross-Site Scripting (XSS)** | Reflected XSS in search inputs and Stored XSS in the user profile/support tickets. |
| **Broken Access Control (IDOR)** | Attackers can view or modify other users' banking transactions by manipulating easily guessable IDs. |
| **Local File Inclusion (LFI)** | The document upload and retrieval endpoints fail to sanitize file paths, allowing server file access. |
| **Insecure File Upload** | Users can upload malicious scripts (.php, .py, .sh) disguised as profile pictures or identity documents. |
| **Weak Authentication** | Missing brute-force protection, predictable session tokens, and lack of 2FA. |
| **Security Misconfiguration** | Debug mode is intentionally left enabled, exposing sensitive backend paths and environment variables. |

---

## ⚙️ Installation & Setup Guide

VulnBank is built using **Python 3** and **Django**. It is designed to be easily deployed locally.

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Mokolthoum/VulnBank.git
cd VulnBank
```

### 2️⃣ Set Up Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Initialize the Database
This will create the SQLite database and apply all necessary models.
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5️⃣ Create an Admin Account (Optional)
To access the Django admin panel (`/admin`):
```bash
python3 manage.py createsuperuser
```

### 6️⃣ Run the Local Server
```bash
python3 manage.py runserver 0.0.0.0:8000
```
**Access the Bank:** Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🛠️ Project Architecture

```text
VulnBank/                   # Root Directory
├── vulnbank/               # Main Django project settings (misconfigured)
├── bank/                   # The primary application logic
│   ├── views.py            # Contains the vulnerable logic (SQLi, IDOR)
│   ├── models.py           # Database schema
│   ├── urls.py             # Endpoint routing
│   └── templates/          # HTML templates (XSS vectors present here)
├── media/                  # Directory for user uploads (Insecure implementation)
├── db.sqlite3              # Database (often accessible via LFI)
└── manage.py               # Django execution script
```

---

## ⚠️ Important Legal & Safety Warning
**DO NOT DEPLOY THIS TO THE INTERNET!**
This software contains devastating security flaws by design. It must **only** be executed in isolated, local environments (localhost) or secure virtual machines. Deploying this application on a public server will result in your system being compromised immediately. The developer assumes no liability for any misuse or damages.
