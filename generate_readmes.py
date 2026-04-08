import os

readme_0x7v11co = """
# 🛡️ 0x7v11co - Advanced Web Vulnerability Scanner

<div align="center">
  <h3>أداة متقدمة لفحص ثغرات الويب واكتشاف نقاط الضعف الأمنية</h3>
  <p>تم تطويرها وتحسينها لتقديم تقارير احترافية وشاملة (عربي/إنجليزي) لمختبري الاختراق.</p>
</div>

---

## 🌟 الميزات (Features)
- **12 موديول فحص متخصص**: يشمل SQLi, XSS, LFI, RCE, اكتشاف الإدارة (Admin Enum)، رفع الملفات وغيرها.
- **تصدير تقارير احترافية**: إمكانية تصدير التقارير بصيغة PDF-ready أو HTML تفاعلية باللغتين العربية والإنجليزية.
- **زاحف الويب (Deep Crawler)**: لاستخراج جميع الروابط المخفية وبناء خريطة كاملة للموقع.
- **تعدد المسارات (Multi-threading)**: أداء فائق السرعة عبر تحديد عدد مسارات الفحص.
- **التخطي (WAF Bypass)**: آليات ذكية لتجاوز جدران الحماية (Web Application Firewalls).
- **فحص معتمد (Authenticated Scan)**: دعم التمرير للكوكيز والجلسات (Cookies/Sessions) لفحص لوحات التحكم.

## 🛠️ المتطلبات (Requirements)
تأكد من توفر Python 3 وأدوات النيتورك الأساسية. يجب تثبيت الحزم المطلوبة قبل البدء:
```bash
pip install -r requirements.txt
```

## 🚀 طريقة التنصيب (Installation)
انسخ هذا المستودع المحلي وابدأ الفحص مباشرة:
```bash
git clone https://github.com/Mokolthoum/0x7v11co.git
cd 0x7v11co
pip install -r requirements.txt
```

## 🎯 الاستخدام (Usage)

### 1️⃣ الفحص الشامل (Comprehensive Scan)
قم بفحص الموقع باستخدام كل الموديولات المتاحة:
```bash
python3 main.py http://example.com --crawl
```

### 2️⃣ الفحص السريع والمخصص (Custom Scan)
يمكنك تحديد ثغرات معينة للبحث عنها بهدف تسريع العملية:
```bash
python3 main.py http://example.com --sqli --xss
```

### 3️⃣ استخراج تقارير باللغة العربية (Arabic Reports)
لتحويل نتائج الفحص إلى تقرير مخصص واحترافي لتقديمه للعملاء:
```bash
# التقرير سيخرج بشكل HTML أو CSV/JSON جاهز للطباعة كـ PDF
python3 main.py http://example.com --html
```

## 📂 بنية المشروع
```
0x7v11co/
├── main.py                 # نقطة الانطلاق لتشغيل الأداة
├── modules/                # موديولات فحص الثغرات المستقلة (12 موديول)
├── utils/                  # أدوات مساعدة (نظام توليد التقارير)
├── requirements.txt        # المتطلبات والمكتبات التشغيلية
└── reports/                # التقارير الناتجة (HTML, JSON, CSV) 
```

---
**تنويه أخلاقي (Disclaimer):**
هذه الأداة مخصصة للاستخدام للمسؤولين عن الحماية والاختبارات الأمنية المصرح بها فقط. المطور غير مسؤول عن أي استخدام غير قانوني.
"""

readme_abaneu = """
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
"""

with open('../0x7v11co/README.md', 'w', encoding='utf-8') as f:
    f.write(readme_0x7v11co)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_abaneu)

print("Readme files generated successfully!")
