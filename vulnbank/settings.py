"""
VulnBank - Django Settings
INTENTIONALLY INSECURE - For vulnerability scanner testing only!
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# VULNERABILITY: Hardcoded secret key
SECRET_KEY = 'django-insecure-v3ry-s3cr3t-k3y-th4t-sh0uld-n0t-b3-h3r3-12345678'

# SECURITY WARNING: don't run with debug turned on in production!
# VULNERABILITY: Debug mode enabled
DEBUG = True

# VULNERABILITY: Accept all hosts
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bank',
]

# VULNERABILITY: Removed SecurityMiddleware, CsrfViewMiddleware, XFrameOptionsMiddleware
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',        # DISABLED - No CSRF protection
    # 'django.middleware.security.SecurityMiddleware',      # DISABLED - No security headers
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',  # DISABLED - Clickjacking possible
]

ROOT_URLCONF = 'vulnbank.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'bank' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vulnbank.wsgi.application'

# Database - SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation - VULNERABILITY: Disabled all validators
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# INTENTIONALLY INSECURE SECURITY SETTINGS
# ============================================

# VULNERABILITY: Session cookie not HTTP-only (accessible via JavaScript)
SESSION_COOKIE_HTTPONLY = False

# VULNERABILITY: Session cookie not secure (sent over HTTP)
SESSION_COOKIE_SECURE = False

# VULNERABILITY: No XSS filter header
SECURE_BROWSER_XSS_FILTER = False

# VULNERABILITY: No content type sniffing protection
SECURE_CONTENT_TYPE_NOSNIFF = False

# VULNERABILITY: No HSTS
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# VULNERABILITY: SSL redirect disabled
SECURE_SSL_REDIRECT = False

# VULNERABILITY: CSRF cookie not secure
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False

# VULNERABILITY: X-Frame-Options not set (allows clickjacking)
X_FRAME_OPTIONS = 'ALLOWALL'

# Login redirect
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
