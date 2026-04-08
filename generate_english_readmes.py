import os

readme_0x7v11co = """# 🛡️ 0x7v11co - Advanced Web Vulnerability Scanner

<div align="center">
  <h3>Advanced Web Vulnerability Scanner and Security Assessment Tool</h3>
  <p>Developed and enhanced to deliver professional, comprehensive reports (PDF-ready/HTML) for penetration testers.</p>
</div>

---

## 🌟 Features
- **12 Dedicated Scanning Modules**: Includes SQLi, XSS, LFI, RCE, Admin Panel Enum, File Upload vulnerabilities, and more.
- **Professional Reporting**: Export beautifully formatted, PDF-ready HTML, CSV, or JSON reports.
- **Deep Web Crawler**: Extract hidden links, map directories, and build a complete site structure.
- **Multi-threading Engine**: Lightning-fast performance with customizable thread counts.
- **WAF Bypass Capabilities**: Intelligent mechanisms to evade and bypass Web Application Firewalls.
- **Authenticated Scanning**: Support for custom cookies and sessions to scan protected admin panels.

## 🛠️ Requirements
Ensure Python 3 and basic networking tools are installed. Install required dependencies before starting:
```bash
pip install -r requirements.txt
```

## 🚀 Installation
Clone this repository locally and start scanning immediately:
```bash
git clone https://github.com/Mokolthoum/0x7v11co.git
cd 0x7v11co
pip install -r requirements.txt
```

## 🎯 Usage

### 1️⃣ Comprehensive Scan
Scan the target using all available modules and the deep crawler:
```bash
python3 main.py http://example.com --crawl
```

### 2️⃣ Custom & Fast Scan
Select specific vulnerabilities to look for, speeding up the process:
```bash
python3 main.py http://example.com --sqli --xss
```

### 3️⃣ Generate Professional Reports
Export your scan results into an interactive HTML or JSON/CSV report ready for clients:
```bash
python3 main.py http://example.com --html --json
```

## 📂 Project Structure
```text
0x7v11co/
├── main.py                 # Initial entry point and engine orchestrator
├── modules/                # 12 Independent vulnerability scanning modules
├── utils/                  # Helper utilities (Reporter, Colors, etc.)
├── requirements.txt        # Python dependencies
└── reports/                # Generated reports directory (HTML, JSON, CSV) 
```

---
**Disclaimer:**
This tool is strictly intended for educational purposes and authorized security testing. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.
"""

readme_abaneu = """# 🏦 VulnBank (AbaNeu)

<div align="center">
  <h3>Intentionally Vulnerable Web Application</h3>
  <p>Dedicated for cybersecurity training, penetration testing, and vulnerability scanner testing.</p>
</div>

---

## 🌟 Overview
**VulnBank** is a simulated banking system designed to contain standard, real-world vulnerabilities (OWASP Top 10). It serves as a safe and legal environment for cybersecurity learners and security tool developers to test their tools and improve their skills.

## 🛡️ Included Vulnerabilities
- SQL Injection (SQLi)
- Cross-Site Scripting (XSS)
- Broken Access Control (Insecure Direct Object References - IDOR)
- Local File Inclusion (LFI)
- Weak Authentication & Session Management

## ⚙️ Installation & Requirements
The application is built using standard Python and the `Django` web framework.

### 1. Install Dependencies
```bash
git clone https://github.com/Mokolthoum/AbaNeu.git
cd AbaNeu
pip install -r requirements.txt
```

### 2. Database Setup (Migrations)
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 3. Create Admin Account (Superuser)
```bash
python3 manage.py createsuperuser
```

### 4. Run the Local Server
```bash
python3 manage.py runserver 0.0.0.0:8000
```
You can now access `http://127.0.0.1:8000/` and begin testing the application using tools like `0x7v11co`!

---
**⚠️ WARNING**: NEVER deploy this application on a public-facing production server. It is intentionally vulnerable and extremely insecure!
"""

with open('../0x7v11co/README.md', 'w', encoding='utf-8') as f:
    f.write(readme_0x7v11co)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_abaneu)

print("English README files generated successfully!")
