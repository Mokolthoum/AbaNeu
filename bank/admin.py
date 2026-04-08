from django.contrib import admin
from .models import UserProfile, Account, Transaction, SupportTicket, UploadedDocument


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'national_id')
    search_fields = ('user__username', 'phone')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'user', 'account_type', 'balance', 'is_active')
    list_filter = ('account_type', 'is_active')
    search_fields = ('account_number', 'user__username')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'sender_account', 'receiver_account', 'amount', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('reference_number', 'description')


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('subject', 'message')


@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at')
    search_fields = ('title', 'description')
