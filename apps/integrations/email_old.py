import email
import imaplib
import re
import smtplib, ssl
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from bs4 import BeautifulSoup
from django.conf import settings
from structlog import get_logger

from apps.integrations.chatgpt import EmailSummary

logger = get_logger()


class Email:
    def __init__(self, user=settings.EMAIL_USER, password=settings.EMAIL_HOST_PASSWORD):
        self.imap = imaplib.IMAP4_SSL(settings.EMAIL_IMAP_URL)
        self.imap.login(user, password)
        self.user = user

    def get_inbox(self, limit=20):
        return self.__get_inbox(limit)

    def summarize_inbox(self, limit=20):
        emails = self.__get_inbox(limit)
        summary = self.__summarize_email(emails)
        self.__send_summary(message=summary)
        return summary

    def __remove_hyperlinks(self, text):
        # Remove URLs starting with http/https
        text = re.sub(r'http\S+', '', text)
        # Remove URLs containing '.com'
        text = re.sub(r'\S+\.com\S*', '', text)
        text = re.sub(r'\S+\.net\S*', '', text)
        text = re.sub(r'\S+\.org\S*', '', text)
        return text

    def __get_inbox(self, limit=5):
        emails = []
        self.imap.select('"[Gmail]/All Mail"', readonly=False)
        response, messages = self.imap.search(None, 'UnSeen')
        messages = messages[0].split()
        order = int(messages[-1])
        for i in range(order, order - limit, -1):
            email_data = {}
            res, msg = self.imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    logger.info("Email", from_=msg['From'], subject=msg['Subject'], date=msg['Date'])
                    email_data['Subject'] = msg['Subject']
                    email_data['From'] = msg['From']
                    email_data['Date'] = msg['Date']
                    email_data['Id'] = msg['Message-ID']

            for part in msg.walk():
                try:
                    text = ""
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        text = body.decode("UTF-8")
                    if part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True)
                        text = body.decode("UTF-8")
                    soup = BeautifulSoup(text, 'html.parser')
                    clean_text = soup.get_text()
                    clean_text = self.__remove_hyperlinks(clean_text)
                    email_data['Body'] = clean_text
                except Exception as e:
                    email_data['Body'] = ""
                    print(e)

            emails.append(email_data)
        return emails

    def __summarize_email(self, emails):
        email_summaries = ""
        summarizer = EmailSummary()
        for em in emails:
            try:
                summary = ""
                text = em['Body']
                if len(text) > 0:
                    summary = summarizer.summarize_email(text)
                    while len(summary.split()) >= 100:
                        # You can adjust the parameters of the email_summarizer function if necessary
                        summary = summarizer.summarize_email(summary)

                else:
                    logger.info("No text found in email")
                email_summaries += f"From: {em['From']}\n"
                email_summaries += f"Subject: {em['Subject']}\n"
                email_summaries += f"Timestamp: {em['Date']}\n"
                email_summaries += f"Link: https://mail.google.com/mail/u/0/#inbox/{em['Id']}\n"
                email_summaries += f"Summary:\n{summary}\n\n\n"
            except:
                traceback.print_exc()
                continue
        return email_summaries

    def __send_summary(self, to=settings.EMAIL_USER, subject="Todogest Summary", message=""):
        logger.info("Sending email summary")
        context = ssl.create_default_context()
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_USER
        msg['To'] = settings.EMAIL_USER
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(settings.EMAIL_USER, settings.EMAIL_HOST_PASSWORD)
            resp = server.send_message(msg)
            server.quit()
            logger.info("Email summary sent", resp=resp)
        logger.info("Email summary sent", resp=resp)
