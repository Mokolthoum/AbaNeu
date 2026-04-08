"""
VulnBank Views - INTENTIONALLY VULNERABLE
Each view implements specific security vulnerabilities for scanner testing.
"""
import os
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from django.conf import settings

from .models import UserProfile, Account, Transaction, SupportTicket, UploadedDocument


# ============================================================
# AUTHENTICATION VIEWS
# ============================================================

def login_view(request):
    """
    VULNERABILITY: SQL Injection in login form.
    Uses raw SQL with string formatting instead of parameterized queries.
    """
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # VULNERABLE: Raw SQL with string interpolation - SQL Injection
        cursor = connection.cursor()
        query = f"SELECT id, username FROM auth_user WHERE username = '{username}' AND password = '{password}'"

        try:
            cursor.execute(query)
            row = cursor.fetchone()
        except Exception:
            row = None

        if row:
            # If SQL injection succeeds, log in as the first matched user
            try:
                user = User.objects.get(id=row[0])
                login(request, user)
                return redirect('/dashboard/')
            except User.DoesNotExist:
                error = "Authentication failed."
        else:
            # Fallback to Django's authenticate for normal login
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard/')
            else:
                error = "Invalid username or password."

    return render(request, 'bank/login.html', {'error': error})


def logout_view(request):
    """Standard logout view."""
    logout(request)
    return redirect('/login/')


# ============================================================
# DASHBOARD & ACCOUNT VIEWS
# ============================================================

@login_required
def dashboard(request):
    """User dashboard showing balance and recent transactions."""
    user = request.user
    accounts = Account.objects.filter(user=user)
    total_balance = sum(acc.balance for acc in accounts)

    # Get recent transactions
    if accounts.exists():
        account_ids = list(accounts.values_list('id', flat=True))
        transactions = Transaction.objects.filter(
            sender_account_id__in=account_ids
        ) | Transaction.objects.filter(
            receiver_account_id__in=account_ids
        )
        transactions = transactions.order_by('-timestamp')[:10]
    else:
        transactions = []

    context = {
        'user': user,
        'accounts': accounts,
        'total_balance': total_balance,
        'transactions': transactions,
    }
    return render(request, 'bank/dashboard.html', context)


# ============================================================
# MONEY TRANSFER (Form Analysis Target)
# ============================================================

@login_required
def transfer_money(request):
    """
    Money transfer form - Target for Form Analysis scanning.
    No CSRF protection (middleware disabled in settings).
    """
    user = request.user
    accounts = Account.objects.filter(user=user)
    message = None
    error = None

    if request.method == 'POST':
        from_account_id = request.POST.get('from_account')
        to_account_number = request.POST.get('to_account_number', '')
        amount = request.POST.get('amount', '0')
        description = request.POST.get('description', '')

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")

            sender_account = Account.objects.get(id=from_account_id, user=user)
            receiver_account = Account.objects.get(account_number=to_account_number)

            if sender_account.balance >= amount:
                sender_account.balance -= amount
                sender_account.save()
                receiver_account.balance += amount
                receiver_account.save()

                Transaction.objects.create(
                    sender_account=sender_account,
                    receiver_account=receiver_account,
                    amount=amount,
                    description=description,
                    reference_number=f"TXN-{uuid.uuid4().hex[:10].upper()}"
                )
                message = f"Successfully transferred ${amount:.2f} to account {to_account_number}."
            else:
                error = "Insufficient balance."
        except Account.DoesNotExist:
            error = "Invalid account number."
        except (ValueError, TypeError) as e:
            error = f"Invalid transfer details: {str(e)}"

    context = {
        'accounts': accounts,
        'message': message,
        'error': error,
    }
    return render(request, 'bank/transfer.html', context)


# ============================================================
# SEARCH TRANSACTIONS (SQL Injection + Reflected XSS)
# ============================================================

@login_required
def search_transactions(request):
    """
    VULNERABILITY: SQL Injection + Reflected XSS.
    - Uses raw SQL with string formatting for search query
    - Echoes the search query back to the page unescaped
    """
    query = request.GET.get('q', '')
    results = []

    if query:
        # VULNERABLE: Raw SQL injection in search
        cursor = connection.cursor()
        sql = f"""
            SELECT t.id, t.amount, t.description, t.timestamp, t.reference_number,
                   sa.account_number as sender_acc, ra.account_number as receiver_acc
            FROM bank_transaction t
            JOIN bank_account sa ON t.sender_account_id = sa.id
            JOIN bank_account ra ON t.receiver_account_id = ra.id
            WHERE t.description LIKE '%{query}%'
               OR t.reference_number LIKE '%{query}%'
               OR sa.account_number LIKE '%{query}%'
               OR ra.account_number LIKE '%{query}%'
            ORDER BY t.timestamp DESC
        """
        try:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            results = []

    # VULNERABILITY: query is passed directly to template and rendered with |safe (Reflected XSS)
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'bank/search.html', context)


# ============================================================
# USER PROFILE (Stored XSS via bio)
# ============================================================

@login_required
def user_profile(request):
    """
    VULNERABILITY: Stored XSS via user bio field.
    Bio is rendered using the |safe filter in the template.
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    accounts = Account.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'accounts': accounts,
    }
    return render(request, 'bank/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile - allows injection of HTML/JS into bio."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # VULNERABLE: No sanitization of bio content
        profile.bio = request.POST.get('bio', '')
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.national_id = request.POST.get('national_id', '')
        profile.save()

        # Handle profile picture upload - VULNERABLE: No file type validation
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()

        return redirect('/profile/')

    context = {'profile': profile}
    return render(request, 'bank/profile_edit.html', context)


# ============================================================
# CUSTOMER SUPPORT (Stored XSS)
# ============================================================

@login_required
def support_page(request):
    """
    VULNERABILITY: Stored XSS via support ticket message.
    Messages are rendered with |safe in the template.
    """
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        # VULNERABLE: No sanitization - stored as-is
        SupportTicket.objects.create(
            user=request.user,
            subject=subject,
            message=message,
        )
        return redirect('/support/')

    tickets = SupportTicket.objects.filter(user=request.user)
    return render(request, 'bank/support.html', {'tickets': tickets})


# ============================================================
# DOCUMENT VIEWER (Local File Inclusion - LFI)
# ============================================================

@login_required
def view_document(request):
    """
    VULNERABILITY: Local File Inclusion (LFI).
    Reads file from disk based on user-supplied 'file' parameter
    with NO path traversal validation.
    """
    file_param = request.GET.get('file', '')
    content = ''
    error = None

    if file_param:
        # VULNERABLE: Direct file read with no validation
        try:
            file_path = os.path.join(settings.BASE_DIR, 'documents', file_param)
            with open(file_path, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            error = f"File '{file_param}' not found."
        except PermissionError:
            error = "Permission denied."
        except Exception as e:
            error = f"Error reading file: {str(e)}"

    # Also list available documents
    documents = UploadedDocument.objects.filter(user=request.user)

    context = {
        'file_param': file_param,
        'content': content,
        'error': error,
        'documents': documents,
    }
    return render(request, 'bank/documents.html', context)


@login_required
def upload_document(request):
    """
    VULNERABILITY: Unrestricted File Upload.
    No validation on file extension or content type.
    """
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled')
        description = request.POST.get('description', '')

        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']

            # VULNERABLE: No file type validation at all
            doc = UploadedDocument.objects.create(
                user=request.user,
                title=title,
                description=description,
                file=uploaded_file,
            )
            return redirect('/documents/view/')

    return render(request, 'bank/upload.html')


# ============================================================
# HIDDEN / RECONNAISSANCE PATHS
# ============================================================

def backup_page(request):
    """Exposed backup directory listing."""
    return render(request, 'bank/backup_index.html')


def dev_logs_page(request):
    """Exposed development logs."""
    log_content = ""
    log_path = os.path.join(settings.BASE_DIR, 'dev_logs', 'debug.log')
    try:
        with open(log_path, 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        log_content = "Log file not found."
    return render(request, 'bank/dev_logs.html', {'log_content': log_content})


def api_users_list(request):
    """VULNERABILITY: Internal API endpoint exposing user data without authentication."""
    users = User.objects.all().values('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    return JsonResponse(list(users), safe=False)


def api_accounts_list(request):
    """VULNERABILITY: Internal API endpoint exposing account data without authentication."""
    accounts = Account.objects.all().values(
        'id', 'user__username', 'account_number', 'account_type', 'balance', 'is_active'
    )
    return JsonResponse(list(accounts), safe=False)


def api_transactions_list(request):
    """VULNERABILITY: Internal API endpoint exposing transaction data without authentication."""
    transactions = Transaction.objects.all().values(
        'id', 'sender_account__account_number', 'receiver_account__account_number',
        'amount', 'description', 'timestamp', 'reference_number'
    )
    return JsonResponse(list(transactions), safe=False)


def robots_txt(request):
    """Robots.txt that reveals hidden directories."""
    content = """User-agent: *
Disallow: /backup/
Disallow: /dev_logs/
Disallow: /api/v1/internal/
Disallow: /admin-panel/
Disallow: /documents/
Disallow: /media/
Sitemap: /sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')


def env_file(request):
    """VULNERABILITY: Exposed .env file with sensitive credentials."""
    env_path = os.path.join(settings.BASE_DIR, '.env.example')
    try:
        with open(env_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = "File not found"
    return HttpResponse(content, content_type='text/plain')


def schema_file(request):
    """VULNERABILITY: Exposed database schema file."""
    schema_path = os.path.join(settings.BASE_DIR, 'database_schema.sql')
    try:
        with open(schema_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = "File not found"
    return HttpResponse(content, content_type='text/plain')


def admin_panel(request):
    """Fake admin panel - another discoverable path."""
    return render(request, 'bank/admin_panel.html')


def sitemap(request):
    """Basic sitemap exposing all URLs."""
    urls = [
        '/login/', '/dashboard/', '/transfer/', '/search/',
        '/profile/', '/support/', '/documents/view/', '/documents/upload/',
        '/backup/', '/dev_logs/', '/api/v1/internal/users/',
        '/api/v1/internal/accounts/', '/api/v1/internal/transactions/',
    ]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'  <url><loc>http://localhost:8000{url}</loc></url>\n'
    xml += '</urlset>'
    return HttpResponse(xml, content_type='application/xml')
