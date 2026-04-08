"""
Seed data management command for VulnBank.
Creates test users, accounts, transactions, and support tickets.
Usage: python manage.py seed_data
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vulnbank.settings')
django.setup()

from django.contrib.auth.models import User
from bank.models import UserProfile, Account, Transaction, SupportTicket
from decimal import Decimal
import uuid


def create_users():
    """Create test users with profiles."""
    users_data = [
        {
            'username': 'admin',
            'password': 'admin123',
            'email': 'admin@vulnbank.local',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
            'bio': 'System administrator for VulnBank. Managing all operations and security.',
            'phone': '+1 (555) 000-0001',
            'address': '123 Admin Street, Secure City, SC 10001',
            'national_id': 'ADM-001-2026',
        },
        {
            'username': 'john',
            'password': 'password123',
            'email': 'john.doe@email.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'is_staff': False,
            'is_superuser': False,
            'bio': 'Hello! I am John Doe, a software engineer based in New York. I have been using VulnBank for my personal savings and daily transactions.',
            'phone': '+1 (555) 123-4567',
            'address': '456 Oak Avenue, Brooklyn, NY 11201',
            'national_id': 'NYC-789-4561',
        },
        {
            'username': 'jane',
            'password': 'password123',
            'email': 'jane.smith@email.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'is_staff': False,
            'is_superuser': False,
            'bio': 'Financial analyst and VulnBank premium customer. Love the convenience of digital banking!',
            'phone': '+1 (555) 987-6543',
            'address': '789 Elm Street, Manhattan, NY 10002',
            'national_id': 'NYC-321-9876',
        },
    ]

    created_users = []
    for data in users_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'is_staff': data['is_staff'],
                'is_superuser': data['is_superuser'],
            }
        )
        if created:
            user.set_password(data['password'])
            user.save()
            print(f"  ✓ Created user: {data['username']} / {data['password']}")
        else:
            print(f"  → User already exists: {data['username']}")

        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'bio': data['bio'],
                'phone': data['phone'],
                'address': data['address'],
                'national_id': data['national_id'],
            }
        )
        created_users.append(user)

    return created_users


def create_accounts(users):
    """Create bank accounts for test users."""
    accounts_data = [
        # Admin accounts
        {'user': users[0], 'account_number': 'VB-1001-0001', 'account_type': 'business', 'balance': Decimal('50000.00')},
        # John's accounts
        {'user': users[1], 'account_number': 'VB-2001-0001', 'account_type': 'savings', 'balance': Decimal('15750.50')},
        {'user': users[1], 'account_number': 'VB-2001-0002', 'account_type': 'checking', 'balance': Decimal('3200.00')},
        # Jane's accounts
        {'user': users[2], 'account_number': 'VB-3001-0001', 'account_type': 'savings', 'balance': Decimal('28900.75')},
        {'user': users[2], 'account_number': 'VB-3001-0002', 'account_type': 'checking', 'balance': Decimal('5600.25')},
    ]

    created_accounts = []
    for data in accounts_data:
        account, created = Account.objects.get_or_create(
            account_number=data['account_number'],
            defaults={
                'user': data['user'],
                'account_type': data['account_type'],
                'balance': data['balance'],
            }
        )
        if created:
            print(f"  ✓ Created account: {data['account_number']} (${data['balance']})")
        else:
            print(f"  → Account already exists: {data['account_number']}")
        created_accounts.append(account)

    return created_accounts


def create_transactions(accounts):
    """Create sample transactions."""
    transactions_data = [
        {'sender': accounts[1], 'receiver': accounts[3], 'amount': Decimal('500.00'),
         'description': 'Monthly rent payment', 'ref': f'TXN-{uuid.uuid4().hex[:10].upper()}'},
        {'sender': accounts[3], 'receiver': accounts[1], 'amount': Decimal('250.00'),
         'description': 'Freelance project payment', 'ref': f'TXN-{uuid.uuid4().hex[:10].upper()}'},
        {'sender': accounts[2], 'receiver': accounts[0], 'amount': Decimal('100.00'),
         'description': 'Service subscription fee', 'ref': f'TXN-{uuid.uuid4().hex[:10].upper()}'},
        {'sender': accounts[0], 'receiver': accounts[2], 'amount': Decimal('2000.00'),
         'description': 'Salary deposit March 2026', 'ref': f'TXN-{uuid.uuid4().hex[:10].upper()}'},
        {'sender': accounts[1], 'receiver': accounts[4], 'amount': Decimal('75.50'),
         'description': 'Dinner split payment', 'ref': f'TXN-{uuid.uuid4().hex[:10].upper()}'},
        {'sender': accounts[4], 'receiver': accounts[1], 'amount': Decimal('1200.00'),
         'description': 'Investment return Q1 2026', 'ref': f'TXN-{uuid.uuid4().hex[:10].upper()}'},
        {'sender': accounts[3], 'receiver': accounts[0], 'amount': Decimal('350.00'),
         'description': 'Consulting payment', 'ref': f'TXN-{uuid.uuid4().hex[:10].upper()}'},
        {'sender': accounts[2], 'receiver': accounts[4], 'amount': Decimal('89.99'),
         'description': 'Online purchase refund', 'ref': f'TXN-{uuid.uuid4().hex[:10].upper()}'},
    ]

    for data in transactions_data:
        txn, created = Transaction.objects.get_or_create(
            reference_number=data['ref'],
            defaults={
                'sender_account': data['sender'],
                'receiver_account': data['receiver'],
                'amount': data['amount'],
                'description': data['description'],
            }
        )
        if created:
            print(f"  ✓ Created transaction: {data['ref']} - ${data['amount']}")


def create_support_tickets(users):
    """Create sample support tickets."""
    tickets_data = [
        {
            'user': users[1],
            'subject': 'Unable to access my savings account',
            'message': 'I have been trying to access my savings account (VB-2001-0001) since yesterday but I keep getting an error message. Please help!',
            'status': 'open',
        },
        {
            'user': users[2],
            'subject': 'Request for account statement',
            'message': 'I need my account statement for the last 3 months for tax purposes. Can you please generate it for my account VB-3001-0001?',
            'status': 'in_progress',
            'response': 'We are working on generating your statement. It will be ready within 24 hours.',
        },
        {
            'user': users[1],
            'subject': 'Suspicious transaction on my account',
            'message': 'I noticed a transaction of $89.99 on my checking account that I did not authorize. Please investigate immediately.',
            'status': 'open',
        },
    ]

    for data in tickets_data:
        ticket, created = SupportTicket.objects.get_or_create(
            subject=data['subject'],
            user=data['user'],
            defaults={
                'message': data['message'],
                'status': data['status'],
                'response': data.get('response', ''),
            }
        )
        if created:
            print(f"  ✓ Created ticket: {data['subject']}")


def main():
    print("\n" + "=" * 50)
    print("  VulnBank - Seed Data Script")
    print("=" * 50)

    print("\n[1/4] Creating users...")
    users = create_users()

    print("\n[2/4] Creating accounts...")
    accounts = create_accounts(users)

    print("\n[3/4] Creating transactions...")
    create_transactions(accounts)

    print("\n[4/4] Creating support tickets...")
    create_support_tickets(users)

    print("\n" + "=" * 50)
    print("  ✓ Seed data created successfully!")
    print("=" * 50)
    print("\n  Test Credentials:")
    print("  ─────────────────")
    print("  admin  / admin123    (superuser)")
    print("  john   / password123 (regular user)")
    print("  jane   / password123 (regular user)")
    print()


if __name__ == '__main__':
    main()
