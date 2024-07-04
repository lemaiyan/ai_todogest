from __future__ import print_function

#from googleapiclient.errors import HttpError
import os
import os.path
import time
import traceback

from django.contrib.auth.models import User
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from structlog import get_logger

from apps.oauth.models import GoogleUserTokens
from apps.todo.models import EmailDigest
from apps.integrations.chatgpt import EmailSummary

logger = get_logger()

import json
import os.path

from django.conf import settings

from apps.integrations.utils.gmail_utils import (chunk_text, create_email,
                                                 get_email_data,
                                                 get_unread_emails,
                                                 mark_as_read,
                                                 mark_as_read_and_archive,
                                                 send_email)

# If modifying these scopes, delete the file token.json.
SCOPES = settings.GOOGLE_OAUTH_SCOPES
home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, '.credentials')
credential_path = os.path.join(credential_dir, 'credentials.json')

class Gmail:
    def __init__(self, email) -> None:
        self.user = User.objects.get(email=email)
        token = None
        self.service = None
        self.email = email
        try:
            token = GoogleUserTokens.objects.get(user__email=email)
            logger.info("Retrieved token", token=token.token)
            logger.info("Refreshing token")
            creds = Credentials(
                **json.loads(token.token)
            )
            logger.info("Retrieved creds", creds=creds)
            if creds and creds.refresh_token:
                creds.refresh(Request())
                token.token = creds.to_json()
                token.save()
                logger.info("Refreshed token", token=token.token)
                self.service = build("gmail", "v1", credentials=creds)
        except GoogleUserTokens.DoesNotExist:
            token = None
            logger.info("Token does not exist you need to connect your gmail", email=email)
            
    def summarize_inbox(self, limit=5):
        emails = self.__get_unread_emails(limit)
        summary = self.__summarize_email(emails)
        self.__send_summary(body=summary)
        return summary
    def get_inbox(self, limit=5):
        emails = self.__get_unread_emails(limit)
        return emails
    def __get_unread_emails(self, limit=5):
        # limit the email fetched to 5
        return get_unread_emails(self.service, limit)
    
    def __send_summary(self, subject="Todogest Summary", body=""):
        logger.info("Sending email summary", subject=subject, body=body)
        email = create_email(self.email, self.email, subject, body)
        return send_email(self.service, email)
    
    def __summarize_email(self, emails):
        total_emails = len(emails)
        email_summaries = ""
        summarizer = EmailSummary()
        for idx, message in enumerate(emails, start=1):
            try:
                email_data = get_email_data(self.service, message['id'])
                logger.info("Trying to summarize email", subject=email_data['subject'])
                if 'text' in email_data and email_data['subject'] is not "Todogest Summary": # we don't summarize a summarized email
                    summary = summarizer.summarize_email(email_data['text'])
                    # Loop until the summary is fewer than 100 words
                    while len(summary.split()) >= 100:
                        summary = summarizer.summarize_email(summary)
                else:
                    summary = ""
                    logger.info("Skipping email with ID {email_data['id']} because no text content was found or was another diget email.")
                
                
                # Add the output to an ongoing list or string called email_summaries
                email_summaries += f"From: {email_data['from']}\n"
                email_summaries += f"Subject: {email_data['subject']}\n"
                email_summaries += f"Timestamp: {email_data['date']}\n"
                email_summaries += f"Link: https://mail.google.com/mail/u/0/#inbox/{message['id']}\n"
                email_summaries += f"Summary:\n{summary}\n\n\n"

                # Mark the summarized emails as read and archived
                if "Skipping email because no text content was found." not in summary and "Email Summaries" not in email_data['subject']:
                    mark_as_read_and_archive(self.service, message['id'])
                if "Email Summaries" in email_data['subject']:
                    mark_as_read(self.service, message['id'])
                
                logger.info(f"({idx} of {total_emails}) emails processed.")
            except:
                logger.info("Error summarizing email", id=message['id'], subject=email_data['subject'])
                traceback.print_exc()
                continue
        EmailDigest.objects.create(user=self.user,summary=email_summaries)
        return email_summaries