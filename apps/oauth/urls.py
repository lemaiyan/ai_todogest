from django.urls import path
from . import views

app_name = "apps.oauth"

urlpatterns = [
    path('google/calendar/init/', views.GoogleCalendarInitView.as_view(), name='google_calendar_init'),
    path('google/calendar/redirect/', views.GoogleCalendarRedirectView, name='google_calendar_redirect'),
    path('outlook/redirect/', views.OutlookRedirectView.as_view(), name='outlook_redirect'),
    path('outlook/login/', views.OutlookInitView.as_view(), name='outlook_login'),
]