import datetime
import os.path
import json

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
    def __int__(self):
        logger.info("Outlook calendar")
        credentials = (settings.OUTLOOK_CLIENT_ID, settings.OUTLOOK_CLIENT_SECRET)
        self.account = Account(credentials, protocol=MSGraphProtocol())
        self.calendar = self.account.schedule()
        self.scopes = ['Calendars.ReadWrite', 'Mail.ReadWrite', 'Mail.Send', 'User.Read']
        if not self.account.is_authenticated:
            self.account.authenticate(scopes=self.scopes)
            logger.info("Authenticated")
    def __add_event(self, title, start_date, end_date, content, email):
        event = self.calendar.new_event(
            subject=title,
            start=start_date,
            end=end_date,
            body=content,
            location=email
        )
        event.save()
        logger.info("Event created", event=event)
        return True, event


    def add_event(self, title, start_date, end_date, content, email):
        added, event = self.__add_event(title, start_date, end_date, content, email)
        logger.info("Adding event")
        return added, event

    def get_events(self):
        events =  self.calendar.get_events()
        logger.info("Events", events=events)
        return events
