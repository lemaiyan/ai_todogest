from apps.oauth.models import GoogleUserTokens
from apps.integrations.gmail import Gmail
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(name='hello_world')
def hello_world():
    print('Hello world!')


@shared_task(name='create_digests')
def create_digests():
    users = GoogleUserTokens.objects.all()
    logger.info(f'Creating digests for {len(users)} users')
    for user in users:
        if user.allow_digest:
            summary = Gmail(user.user.email)
            summary.summarize_inbox(limit=3)