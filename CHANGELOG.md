# 📋 تقرير التحسينات الكامل لأداة 0x7v11co

> **التاريخ:** 2026-04-05  
> **المشروع:** أداة الفحص الأمني [0x7v11co](file:///Users/mohadreamer/0x7v11co)  
> **الهدف:** تحسين الأداة لاكتشاف جميع ثغرات [VulnBank](file:///Users/mohadreamer/AbaNeu)

---

## 📊 النتيجة الإجمالية

| المقياس | قبل التحسين | بعد التحسين |
|---|---|---|
| الثغرات المكتشفة | 9 | **36** |
| أنواع الثغرات | 2 نوعين فقط | **6 أنواع** |
| Risk Score | 26 (HIGH) | **115 (CRITICAL)** |
| نسبة الاكتشاف | ~39% | **~85%+** |
| عدد الملفات المعدلة | 0 | **8 ملفات** |
| ملفات جديدة | 0 | **1 ملف** |

---

## 📁 الملفات المعدلة والإضافات

---

### 1. [main.py](file:///Users/mohadreamer/0x7v11co/main.py) — الملف الرئيسي

**ما تم تغييره:**

#### ✅ إضافة تسجيل دخول تلقائي (Auto-Login)
- أضيفت 3 خيارات جديدة في سطر الأوامر:
  - `--login-url` → رابط صفحة تسجيل الدخول
  - `--username` → اسم المستخدم
  - `--password` → كلمة المرور
- الأداة تقوم تلقائياً بـ:
  1. فتح صفحة Login
  2. استخراج حقول النموذج (username, password, hidden fields)
  3. إرسال بيانات الدخول عبر POST
  4. التحقق من نجاح الدخول (302 redirect + sessionid cookie)
  5. استخدام الـ session cookie في جميع عمليات الفحص اللاحقة

#### ✅ دمج وحدة فحص رفع الملفات
- أضيف `UploadScanner` كوحدة فحص جديدة
- يعمل تلقائياً عند استخدام `--full` أو `--upload`

#### ✅ إزالة التكرارات (Deduplication)
- أضيفت دالة `deduplicate_vulnerabilities()` 
- تزيل الثغرات المتكررة بناءً على: النوع + الرابط + الوصف
- تُشغّل تلقائياً قبل إنشاء التقرير

#### ✅ ترتيب مراحل الفحص
- الـ Auto-Login يعمل **بعد** Phase 1 (Recon) لتجنب مشكلة `database is locked` في SQLite
- الفحص يعمل **بالتتابع** (وليس threads) لحماية الـ session cookies

#### ✅ تتبع النماذج المفحوصة
- أضيف `scanned_form_actions` set لتجنب فحص نفس النموذج مرتين
- الـ Header scan يعمل مرة واحدة فقط (وليس على كل صفحة)

---

### 2. [dir_enum.py](file:///Users/mohadreamer/0x7v11co/modules/dir_enum.py) — اكتشاف المسارات

**ما تم تغييره:**

#### ✅ توسيع قاموس الكلمات (Wordlist)
- **قبل:** 26 كلمة فقط
- **بعد:** 50+ كلمة مصنفة في فئات:

```
الكلمات الجديدة المضافة:
├── المسارات الإدارية: admin-panel, admin_panel, logout
├── صفحات المستخدم: account, accounts
├── الميزات: search, transfer, support, documents, upload
├── الأصول: static, media
├── المسارات الحساسة: backups, database, dev_logs, dev-logs, logs, debug
├── نقاط API: api/v1, api/v2, api/v1/internal/users, 
│              api/v1/internal/accounts, api/v1/internal/transactions
├── الملفات الحساسة: .env.example, .env.backup, .env.local,
│                    .gitignore, .htaccess, sitemap.xml,
│                    database_schema.sql, schema.sql, dump.sql,
│                    db_backup.json, backup.sql
└── أدوات التطوير: server-status, server-info, phpinfo.php,
                   info.php, console, trace
```

---

### 3. [crawler.py](file:///Users/mohadreamer/0x7v11co/modules/crawler.py) — زاحف الويب

**ما تم تغييره:**

#### ✅ تحسين اكتشاف الروابط
- **قبل:** يكتشف `<a href>` فقط ويتوقف عند status ≠ 200
- **بعد:**
  - يتبع **Redirects** (302, 301) ويُضيف الوجهة النهائية
  - يستخرج **form actions** كروابط إضافية
  - يبحث عن URLs في **JavaScript** (regex pattern matching)
  - يتجاهل المزيد من الملفات الثابتة (.jpeg, .ico, .woff, .ttf, .eot)

#### ✅ زيادة العمق
- **قبل:** `max_depth = 2`
- **بعد:** `max_depth = 3`

#### ✅ تحسين URL normalization
- إزالة trailing slash للمقارنة
- تجنب زيارة نفس الرابط مرتين

---

### 4. [form_scan.py](file:///Users/mohadreamer/0x7v11co/modules/form_scan.py) — فحص النماذج

**ما تم تغييره:**

#### ✅ كشف CSRF المفقود
- يفحص كل نموذج POST بحثاً عن tokens الحماية:
  - `csrfmiddlewaretoken` (Django)
  - `csrf_token`, `_token` (Laravel)
  - `authenticity_token` (Rails)
  - `__RequestVerificationToken` (.NET)
- يُبلّغ عن النماذج بدون حماية كثغرة `CSRF Missing` (Medium)

#### ✅ كشف حقول رفع الملفات
- يحدد النماذج التي تحتوي `<input type="file">`
- يُخزن المعلومة لاستخدامها من UploadScanner

#### ✅ دعم عناصر إضافية
- أضيف دعم `<textarea>` و `<select>` بالإضافة لـ `<input>`

---

### 5. [header_scan.py](file:///Users/mohadreamer/0x7v11co/modules/header_scan.py) — فحص الأمان

**ما تم تغييره:**

#### ✅ فحص أمان Cookies
- يفحص **HttpOnly flag** — هل JavaScript يستطيع قراءة الـ cookie؟
- يفحص **Secure flag** — هل الـ cookie تُرسل فقط عبر HTTPS؟
- يُبلّغ عن كل cookie غير آمن كثغرة `Insecure Cookie`

---

### 6. [sqli_scan.py](file:///Users/mohadreamer/0x7v11co/modules/sqli_scan.py) — فحص SQL Injection

**ما تم تغييره:**

#### ✅ كشف Login Bypass
- **قبل:** يبحث فقط عن رسائل خطأ SQL في الاستجابة
- **بعد:** يقارن استجابة payload SQLi مع استجابة عادية:
  - إذا كان SQLi يُرجع 302 (redirect) والعادي يُرجع 200 → **Login Bypass!**
  - إذا كان حجم الاستجابة مختلف بشكل كبير → احتمال SQL Injection

#### ✅ إضافة أخطاء Django/Python
```
الأخطاء الجديدة المكتشفة:
- operationalerror, programming error
- syntax error, near "
- unrecognized token, no such column
- database is locked
- sqlite3.operationalerror, django.db.utils
- psycopg2, pymysql
```

#### ✅ Boolean-Blind SQLi Detection
- يُرسل `' AND 1=1 --` (TRUE) و `' AND 1=2 --` (FALSE)
- يقارن حجم الاستجابة: إذا كان الفرق > 50 bytes → SQLi!

#### ✅ توسيع Payloads
- أُضيف: `Union Select`, `Error Based (')`
- تحسين: معالجة hidden fields بشكل صحيح

---

### 7. [lfi_scan.py](file:///Users/mohadreamer/0x7v11co/modules/lfi_scan.py) — فحص Local File Inclusion

**ما تم تغييره:**

#### ✅ اكتشاف Parameters في الصفحة
- **قبل:** يفحص الـ URL parameters الحالية فقط
- **بعد:** يبحث في الصفحة عن **جميع الروابط** التي تحتوي parameters مشابهة لأسماء ملفات:
  ```
  file, page, doc, document, path, include, 
  template, view, content, load, read, url, filename
  ```
- مثال: إذا وجد رابط `href="/documents/view/?file=terms.txt"` → يُختبر مع payloads الـ LFI

#### ✅ Payloads متنوعة
```
../../../../etc/passwd
/etc/passwd
C:\Windows\win.ini
....//....//....//etc/passwd
..%2f..%2f..%2f..%2fetc%2fpasswd
```

---

### 8. [upload_scan.py](file:///Users/mohadreamer/0x7v11co/modules/upload_scan.py) — 🆕 ملف جديد!

**ما تم إنشاؤه:**

#### ✅ فحص رفع ملفات خطيرة
- يبحث عن نماذج تحتوي `<input type="file">`
- يحاول رفع 3 أنواع ملفات خطيرة:

| الملف | النوع | لماذا خطير؟ |
|---|---|---|
| `test_scan.php` | PHP Web Shell | تنفيذ كود على السيرفر |
| `test_scan.exe` | Executable | برنامج ضار |
| `test_scan.html` | HTML + JS | XSS مخزّن |

- يجمع بيانات النموذج تلقائياً (hidden inputs, textareas)
- يكتشف النجاح عبر: status code 200/302 + كلمات مثل "success"/"uploaded"

---

### 9. [reporter.py](file:///Users/mohadreamer/0x7v11co/utils/reporter.py) — التقارير

**ما تم تغييره:**

#### ✅ OWASP Mappings جديدة
```
CSRF Missing          → A01:2021-Broken Access Control
Insecure Cookie       → A05:2021-Security Misconfiguration  
Unrestricted Upload   → A04:2021-Insecure Design
Missing Security Header → A05:2021-Security Misconfiguration
```

#### ✅ نصائح الإصلاح (Remediation) الجديدة
- **CSRF:** أضف `{% csrf_token %}` في Django templates
- **Cookies:** فعّل `SESSION_COOKIE_HTTPONLY=True` و `SESSION_COOKIE_SECURE=True`
- **Upload:** قيّد الامتدادات المسموحة على السيرفر
- **SQLi:** استخدم Django ORM بدلاً من raw SQL

---

## 🛠️ دليل حل المشاكل

---

### المشكلة 1: `Auto-login failed`

**السبب:** قاعدة بيانات SQLite مقفلة (`database is locked`) بسبب اتصالات سابقة لم تُغلق.

**الحل:**
```bash
# الخطوة 1: أوقف سيرفر Django
kill $(lsof -i :8000 -t) 2>/dev/null

# الخطوة 2: انتظر ثانيتين
sleep 2

# الخطوة 3: أعد تشغيل السيرفر
cd /Users/mohadreamer/AbaNeu
source venv/bin/activate
python3 manage.py runserver 8000 &

# الخطوة 4: انتظر حتى يبدأ السيرفر
sleep 3

# الخطوة 5: شغّل الفحص مرة أخرى
```

---

### المشكلة 2: `Connection refused` أو `ConnectTimeout`

**السبب:** السيرفر غير مشغّل.

**الحل:**
```bash
# تحقق أن السيرفر يعمل
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/login/
# يجب أن يُعطي: 200

# إذا لم يعمل، شغّله:
cd /Users/mohadreamer/AbaNeu
source venv/bin/activate
python3 manage.py runserver 8000 &
```

---

### المشكلة 3: `That port is already in use`

**السبب:** شيء آخر يستخدم البورت 8000.

**الحل:**
```bash
# اكتشف العملية التي تستخدم البورت
lsof -i :8000

# أوقفها
kill -9 $(lsof -i :8000 -t)

# ثم أعد التشغيل
sleep 2
cd /Users/mohadreamer/AbaNeu && source venv/bin/activate
python3 manage.py runserver 8000 &
```

---

### المشكلة 4: `ModuleNotFoundError`

**السبب:** مكتبة Python غير مثبتة.

**الحل:**
```bash
cd /Users/mohadreamer/0x7v11co
source venv/bin/activate
pip install beautifulsoup4 requests rich
```

---

### المشكلة 5: التقرير لا يُظهر ثغرات كثيرة (فقط Headers و Directories)

**السبب:** الـ Auto-login فشل فالأداة لم تصل للصفحات المحمية.

**الحل:** 
1. أوقف السيرفر وأعد تشغيله (المشكلة 1)
2. تأكد أن بيانات الدخول صحيحة
3. أعد الفحص

---

### المشكلة 6: `SyntaxError` عند تشغيل الأداة

**السبب:** خطأ في ترميز ملف Python.

**الحل:**
```bash
# تحقق من الأخطاء
cd /Users/mohadreamer/0x7v11co
python3 -c "import py_compile; py_compile.compile('main.py', doraise=True)"
python3 -c "import py_compile; py_compile.compile('modules/upload_scan.py', doraise=True)"
```

---

## 🚀 أوامر التشغيل

---

### الأمر الكامل للفحص الشامل (مع تسجيل الدخول):
```bash
cd /Users/mohadreamer/0x7v11co && source venv/bin/activate && python3 main.py http://127.0.0.1:8000 --full --verbose --export all --login-url http://127.0.0.1:8000/login/ --username john --password password123
```

### شرح كل خيار:

| الخيار | الشرح |
|---|---|
| `http://127.0.0.1:8000` | رابط الموقع المراد فحصه |
| `--full` | فحص شامل (كل الوحدات) |
| `--verbose` أو `-v` | عرض تفاصيل الفحص أثناء التشغيل |
| `--export all` | تصدير النتائج بكل الصيغ (JSON, CSV, Markdown) |
| `--login-url http://...` | رابط صفحة تسجيل الدخول |
| `--username john` | اسم المستخدم |
| `--password password123` | كلمة المرور |

### أوامر بديلة:

```bash
# فحص سريع (بدون تسجيل دخول):
python3 main.py http://127.0.0.1:8000 --fast

# فحص محدد (SQLi + XSS فقط):
python3 main.py http://127.0.0.1:8000 --sqli --xss

# فحص مع ملف تصدير مخصص:
python3 main.py http://127.0.0.1:8000 --full --output my_report --export json

# فحص مع cookie يدوية (بدلاً من auto-login):
python3 main.py http://127.0.0.1:8000 --full --cookie "sessionid=abc123"

# فحص Directory فقط:
python3 main.py http://127.0.0.1:8000 --dir-enum --verbose

# فحص رفع الملفات فقط:
python3 main.py http://127.0.0.1:8000 --upload --login-url http://127.0.0.1:8000/login/ --username john --password password123
```

### جميع الخيارات المتاحة:

```
الخيار               الوظيفة
─────────────────────────────────────────────
--full               فحص شامل (كل الوحدات)
--fast               فحص سريع (Headers + Forms + WP)
--headers            فحص Security Headers
--forms              اكتشاف النماذج + CSRF
--sqli               فحص SQL Injection
--xss                فحص XSS
--lfi                فحص Local File Inclusion
--dir-enum           اكتشاف المسارات
--fuzz               Input Fuzzing
--wp-scan            كشف WordPress
--crawl              زحف الموقع
--subdomains         اكتشاف النطاقات الفرعية
--ports              فحص البورتات
--proxy              كشف Proxy/WAF
--upload             فحص رفع الملفات
--login-url URL      رابط صفحة الدخول
--username USER      اسم المستخدم
--password PASS      كلمة المرور
--cookie COOKIE      Cookies يدوية
--export FORMAT      تصدير (json/csv/md/all)
--threads N          عدد الخيوط (الافتراضي: 5)
--output NAME        اسم ملف التقرير
--verbose / -v       عرض التفاصيل
```

---

## 📌 نصيحة أخيرة

**قبل كل فحص، تأكد من:**
1. ✅ سيرفر Django يعمل (`curl http://127.0.0.1:8000/login/`)
2. ✅ أنت في بيئة venv الخاصة بالأداة (`source venv/bin/activate`)
3. ✅ بيانات الدخول صحيحة
