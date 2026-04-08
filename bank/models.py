from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile with bio (Stored XSS target) and profile picture."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.TextField(blank=True, default='')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return f"Profile of {self.user.username}"


class Account(models.Model):
    """Bank account linked to a user."""
    ACCOUNT_TYPES = [
        ('savings', 'Savings Account'),
        ('checking', 'Checking Account'),
        ('business', 'Business Account'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='savings')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.account_number} ({self.user.username}) - ${self.balance}"


class Transaction(models.Model):
    """Transaction records between accounts."""
    sender_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='sent_transactions'
    )
    receiver_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='received_transactions'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_number = models.CharField(max_length=30, blank=True, default='')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"${self.amount} from {self.sender_account.account_number} to {self.receiver_account.account_number}"


class SupportTicket(models.Model):
    """Customer support tickets - Stored XSS target via subject and message."""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket: {self.subject} ({self.user.username})"


class UploadedDocument(models.Model):
    """User-uploaded documents - Unrestricted file upload vulnerability."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
