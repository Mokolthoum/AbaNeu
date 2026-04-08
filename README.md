# 🏦 VulnBank (AbaNeu)

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
