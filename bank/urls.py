from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Core Banking
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transfer/', views.transfer_money, name='transfer'),
    path('search/', views.search_transactions, name='search'),

    # User Profile
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Customer Support (Stored XSS)
    path('support/', views.support_page, name='support'),

    # Documents (LFI + File Upload)
    path('documents/view/', views.view_document, name='view_document'),
    path('documents/upload/', views.upload_document, name='upload_document'),

    # Hidden / Reconnaissance paths
    path('backup/', views.backup_page, name='backup'),
    path('dev_logs/', views.dev_logs_page, name='dev_logs'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    # Internal API endpoints (no authentication required)
    path('api/v1/internal/users/', views.api_users_list, name='api_users'),
    path('api/v1/internal/accounts/', views.api_accounts_list, name='api_accounts'),
    path('api/v1/internal/transactions/', views.api_transactions_list, name='api_transactions'),

    # Exposed files
    path('robots.txt', views.robots_txt, name='robots'),
    path('.env.example', views.env_file, name='env_file'),
    path('database_schema.sql', views.schema_file, name='schema_file'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
]
