from django.contrib.auth import login as django_login
from django.shortcuts import redirect, reverse
from structlog import get_logger
log = get_logger()


def pre_login_user(user, request):
   log.info("Pre login user", user=user)
   if not user.is_active:
       log.info("User is not active", user=user)
       return redirect(reverse("apps.ui:login"))
   if user.email != "jijolemaiyam@gmail.com": 
        django_login(request, user)
        return redirect(reverse("apps.ui:dashboard"))