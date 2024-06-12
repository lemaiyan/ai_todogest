from django.contrib import admin
from .models import GoogleCreds, GoogleUserTokens, GoogleUser


# Register your models here.

@admin.register(GoogleCreds)
class GoogleCredsAdmin(admin.ModelAdmin):
    list_display = ('app_name','credentials', 'created_at', 'updated_at')
    search_fields = ('credentials',)
    ordering = ('created_at',)


@admin.register(GoogleUserTokens)
class GoogleUserTokensAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'updated_at')
    search_fields = ('user',)
    ordering = ('created_at',)

@admin.register(GoogleUser)
class GoogleUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'google_user_id', 'verified_email', 'locale', 'photo', 'created_at')
    search_fields = ('user',)
    ordering = ('created_at',)