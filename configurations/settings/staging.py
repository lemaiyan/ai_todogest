from .base import *
DEBUG = True
CSRF_TRUSTED_ORIGINS = ['https://todogest.eastus.cloudapp.azure.com']
OUTLOOK_REDIRECT_URIS = 'https://todogest.eastus.cloudapp.azure.com/oauth/outlook/redirect/'
GOOGLE_REDIRECT_URIS ='https://todogest.eastus.cloudapp.azure.com/oauth/google/calendar/redirect/'