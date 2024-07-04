import datetime
import json
import os.path

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

from apps.oauth.models import GoogleUserTokens, GoogleUser

logger = get_logger()

SCOPES = settings.GOOGLE_OAUTH_SCOPES
home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, '.credentials')
credential_path = os.path.join(credential_dir, 'credentials.json')

REDIRECT_URI = 'http://localhost/google/calendar/redirect/'

CLIENT_SECRETS_FILE = credential_path


def GoogleCalendarInitView(request, user_email):
    logger.info("Initializing Google Calendar")
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='false'
    )

    request.session['oauth_state'] = state  # Save the state so the callback can verify the auth server response.
    request.session['user_email'] = user_email
    logger.info("Redirecting to Google Calendar", url=authorization_url, state=state, user_email=user_email)

    return redirect(authorization_url)

def GoogleCalendarRedirectView(request):
    logger.info("Redirecting to Google Calendar")
    state = request.session.pop('oauth_state', '')
    user_email = request.session.pop('user_email', '')
    logger.info("Retrieved state and user email", state=state, user_email=user_email)
    current_user = User.objects.get(email=user_email)
    token = None
    try:
        token = GoogleUserTokens.objects.get(user__email=user_email)
        logger.info("Retrieved token", token=token.token)
    except GoogleUserTokens.DoesNotExist:
        token = None
        logger.info("Token does not exist")
    if not token:
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

        flow.fetch_token(authorization_response=authorization_response) # Fetches the access token
        credentials = flow.credentials
        logger.info("Created token", token=credentials.to_json())
        session = flow.authorized_session()
        user_info = session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        user, created=User.objects.get_or_create(
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
                #locale=user_info['locale'],
                photo=user_info['picture']
            )
        GoogleUserTokens.objects.create(user=user, token=credentials.to_json())
        django_login(request, user)
        return redirect(reverse('apps.ui:dashboard'))
    else:
        logger.info("Refreshing token")
        creds = google.oauth2.credentials.Credentials(
            **json.loads(token.token)
        )
        logger.info("Retrieved creds", creds=creds)
        if creds and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
            token.token = creds.to_json()
            token.save()
            logger.info("Refreshed token", token=token.token)
        logger.info("Returning refreshed token")
        django_login(request, current_user)
        return redirect(reverse('apps.ui:dashboard'))