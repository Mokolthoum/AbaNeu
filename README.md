
# 🏦 VulnBank (AbaNeu)

<div align="center">
  <h3>تطبيق بنكي غير آمن (Vulnerable Web Application)</h3>
  <p>مخصص لأغراض التدريب على أمن المعلومات واختبارات الاختراق.</p>
</div>

---

## 🌟 نظرة عامة (Overview)
تطبيق **VulnBank** هو محاكاة لنظام بنكي تم تصميمه خصيصاً بحيث يحتوي على ثغرات أمنية شائعة (OWASP Top 10) ليتمكن متعلمي أمن المعلومات ومطوري الأدوات الأمنية من اختباره وتحسين مهاراتهم في بيئة آمنة وقانونية.

## 🛡️ الثغرات الموجودة (Vulnerabilities Included)
- SQL Injection (SQLi)
- Cross-Site Scripting (XSS)
- Broken Access Control (Insecure Direct Object References - IDOR)
- Local File Inclusion (LFI)
- Weak Authentication / Session Management

## ⚙️ المتطلبات وطريقة التثبيت (Installation)
يعتمد التطبيق على إطار عمل `Django` بلغة بايثون.

### 1- تنصيب المكتبات
```bash
git clone https://github.com/Mokolthoum/AbaNeu.git
cd AbaNeu
pip install -r requirements.txt
```

### 2- إعداد قواعد البيانات (Migrations)
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 3- عمل حساب مدير (Superuser)
```bash
python3 manage.py createsuperuser
```

### 4- تشغيل السيرفر (Run Server)
```bash
python3 manage.py runserver 0.0.0.0:8000
```
الآن يمكنك زيارة `http://127.0.0.1:8000/` والبدء بعملية الفحص عن طريق الأدوات مثل `0x7v11co`!

---
**⚠️ تحذير**: لا تقم برفع هذا الموقع على خادم إنتاج (Production Server) مفتوح للعامة إطلاقاً، لأنه غير آمن عمدًا!
