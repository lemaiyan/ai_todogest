import json
from datetime import datetime, timedelta
from O365.utils.token import BaseTokenBackend
from apps.oauth.models import OutlookUserTokens
from structlog import get_logger

logger = get_logger()


class DjangoTokenBackend(BaseTokenBackend):
    def __init__(self, user):
        self.user = user
        super().__init__()

    def load_token(self):
        logger.info("Getting token")
        try:
            token = OutlookUserTokens.objects.get(user=self.user)
            token_dict = {
                'token_type': token.token_type,
                'access_token': token.access_token,
                'refresh_token':token.refresh_token,
                'expires_in': token.expires_in,
                'expires_at': token.expires_at
            }
            logger.info("Retrieved token", token=token_dict)
            return self.token_constructor(token_dict)
        except OutlookUserTokens.DoesNotExist:
            logger.info("Token does not exist")
            return None

    def save_token(self):
        logger.info("Saving token")

        if not self.token:
            raise ValueError("Token is not set")

        try:
            logger.info("Token", token=self.serializer.dumps(self.token))
            OutlookUserTokens.objects.filter(user=self.user).update(**self.token)
            logger.info("Saved token")
            return True
        except OutlookUserTokens.DoesNotExist:
            logger.info("Token does not exist")
            return False