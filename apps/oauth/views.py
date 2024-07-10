import datetime
import json
import os.path
import os

from django.views import View
import google.auth.transport.requests
import google.oauth2.credentials
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from structlog import get_logger
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from O365 import Account, MSGraphProtocol

from apps.oauth.models import GoogleUserTokens, GoogleUser, OutlookUserTokens

logger = get_logger()

SCOPES = settings.GOOGLE_OAUTH_SCOPES
home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, '.credentials')
credential_path = os.path.join(credential_dir, 'credentials.json')

REDIRECT_URI = settings.GOOGLE_REDIRECT_URIS

CLIENT_SECRETS_FILE = credential_path

CLIENT_ID = settings.OUTLOOK_CLIENT_ID,
CLIENT_SECRET = settings.OUTLOOK_CLIENT_SECRET
AUTHORITY = 'https://login.microsoftonline.com/2bc9faed-d87c-43e7-af55-fab8edb478a9'
OUTLOOK_REDIRECT_URI = settings.OUTLOOK_REDIRECT_URIS
OUTLOOK_SCOPES = settings.OUTLOOK_SCOPES


class GoogleCalendarInitView(View):
    def get(self, request):
        logger.info("Initializing Google Calendar")
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        logger.info("Redirecting to Google Calendar", authorization_url=authorization_url, state=state)
        request.session['oauth_state'] = state
        return redirect(authorization_url)


def GoogleCalendarRedirectView(request):
    logger.info("Redirecting to Google Calendar")
    state = request.session.pop('oauth_state', '')
    logger.info("Retrieved state and user email", state=state)
    if state != request.GET.get('state', ''):
        pass
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=state
    )
    authorization_response = request.build_absolute_uri()
    authorization_response = authorization_response.replace("http", "https")

    flow.fetch_token(authorization_response=authorization_response)  # Fetches the access token
    credentials = flow.credentials
    logger.info("Created token", token=credentials.to_json())
    session = flow.authorized_session()
    user_info = session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    user, created = User.objects.get_or_create(
        email=user_info['email'],
        defaults={
            'first_name': user_info['given_name'],
            'last_name': user_info['family_name'],
            'is_active': True
        }
    )
    logger.info("User info", user_info=user_info)

    GoogleUser.objects.update_or_create(
        user=user,
        google_user_id=user_info['id'],
        verified_email=user_info['verified_email'],
        # locale=user_info['locale'],
        photo=user_info['picture']
    )
    GoogleUserTokens.objects.create(user=user, token=credentials.to_json())
    django_login(request, user)
    return redirect(reverse('apps.ui:dashboard'))


class OutlookInitView(View):
    def get(self, request):
        logger.info("Initializing Outlook", client_id=settings.OUTLOOK_CLIENT_ID,
                    client_secret=settings.OUTLOOK_CLIENT_SECRET)
        credentials = (settings.OUTLOOK_CLIENT_ID, settings.OUTLOOK_CLIENT_SECRET)
        account = Account(credentials, protocol=MSGraphProtocol())
        url, state = account.con.get_authorization_url(
            requested_scopes=OUTLOOK_SCOPES, redirect_uri=OUTLOOK_REDIRECT_URI
        )
        logger.info("Redirecting to Outlook", url=url, state=state)
        request.session['oauth_state'] = state
        return redirect(url)


class OutlookRedirectView(View):
    def get(self, request):
        credentials = (settings.OUTLOOK_CLIENT_ID, settings.OUTLOOK_CLIENT_SECRET)
        account = Account(credentials, protocol=MSGraphProtocol())
        state = request.session.get('oauth_state', '')
        requested_url = request.build_absolute_uri()
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        result = account.con.request_token(requested_url, state=state, redirect_uri=OUTLOOK_REDIRECT_URI)
        if not result:
            messages.error(request, "Failed to authenticate with Microsoft")
            return JsonResponse({"error": "Failed to authenticate with Microsoft"}, status=400)
        else:
            logger.info("Retrieved token", token=result)
            token = account.con.token_backend.get_token()
            user = account.get_current_user()
            current_user = None
            try:
                logger.info("Retrieved user", user=user, token=token)
                current_user = User.objects.get(email=user.mail)
            except User.DoesNotExist:
                logger.info("User does not exist")
                current_user = User.objects.create_user(
                    username=user.mail,
                    email=user.mail,
                    first_name=user.given_name,
                    last_name=user.surname,
                    is_active=True
                )
                logger.info("Created user", user=current_user)

            try:
                logger.info("Retrieved token", token=token)
                OutlookUserTokens.objects.filter(user=current_user).update(**token)
                logger.info("Updated token", token=token)
            except OutlookUserTokens.DoesNotExist:
                logger.info("Token does not exist")
                token['user'] = current_user
                OutlookUserTokens.objects.create(**token)
                logger.info("Created token", token=token)

            django_login(request, current_user)
            return redirect(reverse('apps.ui:dashboard'))
