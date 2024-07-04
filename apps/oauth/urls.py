from django.urls import path
from . import views

app_name = "apps.google_oauth"

urlpatterns = [
    path('calendar/init/<user_email>/', views.GoogleCalendarInitView, name='calendar_init'),
    path('calendar/redirect/', views.GoogleCalendarRedirectView, name='calendar_redirect'),
]