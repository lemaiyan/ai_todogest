import datetime
import os.path
import json
import datetime as dt


from O365 import Account, MSGraphProtocol
from django.conf import settings
from django.contrib.auth.models import User
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from structlog import get_logger

from apps.oauth.models import GoogleUserTokens
from apps.integrations.utils.outlook_utils import DjangoTokenBackend

logger = get_logger()

# If modifying these scopes, delete the file token.json.
SCOPES = settings.GOOGLE_OAUTH_SCOPES
home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, '.credentials')
credential_path = os.path.join(credential_dir, 'credentials.json')

class GMailCalendar:
    def __init__(self, email) -> None:
        current_user = User.objects.get(email=email)
        token = None
        self.service = None
        try:
            token = GoogleUserTokens.objects.get(user__email=email)
            logger.info("Retrieved token", token=token.token)
            logger.info("Refreshing token")
            creds = Credentials(
                **json.loads(token.token)
            )
            logger.info("Retrieved creds", creds=creds)
            self.service = build("calendar", "v3", credentials=creds)
            if creds and creds.refresh_token:
                creds.refresh(Request())
                token.token = creds.to_json()
                token.save()
                logger.info("Refreshed token", token=token.token)
                self.service = build("calendar", "v3", credentials=creds)
        except GoogleUserTokens.DoesNotExist:
            token = None
            logger.info("Token does not exist you need to connect your calendar", email=email)
    def __add_event(self, title, start_date, end_date, content, email):
        try:
            calendar_event = {
                'summary': title,
                'description': content,
                'start': {
                    'dateTime': start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': 'Africa/Nairobi',
                },
                'end': {
                    'dateTime': end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': 'Africa/Nairobi',
                },
                'attendees': [
                    {'email':  f"{email}"},
                ],
                'reminders': {
                    'useDefault': True,         
                }
            }
            event = self.service.events().insert(calendarId='primary', body=calendar_event).execute()
            logger.info("Event created", calendar_event=event)
            return True, event
        except HttpError as err:
            logger.error("Error creating event", err=err)
            return False, None
    def add_event(self, title, start_date, end_date, content, email):
        logger.info("Adding event")
        added, event = self.__add_event(title, start_date, end_date, content, email)
        return added, event



class OutlookCalendar:
    def __init__(self, email):
        self.user = User.objects.get(email=email)
        logger.info("Outlook calendar")
        credentials = (settings.OUTLOOK_CLIENT_ID, settings.OUTLOOK_CLIENT_SECRET)
        token_backend = DjangoTokenBackend(self.user)
        self.account = Account(credentials, protocol=MSGraphProtocol(), token_backend=token_backend)
        self.calendar = self.account.schedule()
        if not self.account.is_authenticated:
            self.account.con.refresh_token()
            logger.info("Token refreshed")

    def add_event(self, subject, body):
        logger.info("Adding event")
        start_date = dt.datetime.now()
        end_date = dt.datetime.now() + dt.timedelta(hours=1)
        event = self.calendar.new_event()
        try:

            event.subject = subject
            event.start = start_date
            event.end = end_date
            event.body = body
            event.location = "Online"
            event.save()
            return True, event
        except Exception as error:
            logger.error("Error creating event", error=error)
            raise ValueError("Error creating event")


