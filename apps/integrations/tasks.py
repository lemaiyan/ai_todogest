from apps.oauth.models import GoogleUserTokens, OutlookUserTokens
from django.contrib.auth.models import User
from apps.integrations.email import Gmail, OutlookEmail
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(name='hello_world')
def hello_world():
    print('Hello world!')


@shared_task(name='create_digests')
def create_digests():
    users = User.objects.all()
    logger.info(f'Creating digests for {len(users)} users')
    for user in users:
        if user.email.endswith('@gmail.com'):
            token = GoogleUserTokens.objects.filter(user=user).last()
            if token and token.allow_digest:
                summary = Gmail(user.email)
                summary.summarize_inbox(limit=3)
        else:
            token = OutlookUserTokens.objects.filter(user=user).last()
            if token and token.allow_digest:
                summary = OutlookEmail(user.email)
                summary.summarize_inbox(limit=3)