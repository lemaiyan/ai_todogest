from django.db import models
from django.contrib.auth.models import User


class GoogleCreds(models.Model):
    app_name = models.CharField(max_length=255, null=True, blank=True)
    credentials = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.credentials

    class Meta:
        verbose_name_plural = 'Google Creds'


class GoogleUserTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(null=True, blank=True)
    allow_digest = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'Google User Tokens'
        
class GoogleUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    google_user_id = models.CharField(max_length=255, null=True, blank=True)
    verified_email = models.BooleanField(default=False)
    locale = models.CharField(max_length=255, null=True, blank=True)
    photo= models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'Google User'
