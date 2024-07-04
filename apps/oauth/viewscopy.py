from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
import json
import os.path
import google.oauth2.credentials
import google.auth.transport.requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow

SCOPES = ['https://www.googleapis.com/auth/calendar',
          "https://www.googleapis.com/auth/userinfo.profile",
          "openid", "https://www.googleapis.com/auth/userinfo.email"
          "https://www.googleapis.com/auth/calendar.readonly"]
home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, '.credentials')
credential_path = os.path.join(credential_dir, 'credentials.json')

REDIRECT_URI = 'http://localhost/google/calendar/redirect/'

CLIENT_SECRETS_FILE = credential_path


def GoogleCalendarInitView(request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['oauth_state'] = state  # Save the state so the callback can verify the auth server response.

    return redirect(authorization_url)

def GoogleCalendarRedirectView(request):
    state = request.session.pop('oauth_state', '')
    if state != request.GET.get('state', ''):
        pass
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=state
    )
    authorization_response = request.build_absolute_uri()
    authorization_response = authorization_response.replace("http", "https")

    flow.fetch_token(authorization_response=authorization_response) # Fetches the access token
    credentials = flow.credentials

    # Get list of events [Starting from 1st May 2023 to 31st May 2023]
    # Added parameters "timeMin="2023-05-01T00:00:00+05:30", timeMax="2023-05-31T23:59:59+05:30"" to get events only for the month of May 2023

    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary', maxResults=10, orderBy = "updated", singleEvents=True, timeMin="2023-05-01T00:00:00+05:30", timeMax="2023-05-31T23:59:59+05:30").execute()
    events = events_result.get('items', [])

    # Sort events based on start time in descending order
    events = sorted(events, key=lambda event: event['start'].get('dateTime', event['start'].get('date')), reverse=True)

    # Iterate over the events and extract the day, month, and year
    for event in events:
        start_time = event['start'].get('dateTime')
        if start_time:
            date_parts = start_time.split('T')[0].split('-')
            day = date_parts[2]
            month = date_parts[1]
            year = date_parts[0]
            formatted_date = f'{day}/{month}/{year}'
            event['formatted_date'] = formatted_date

    # Render the events in a basic HTML page
    if events:
        # Pass the events data to the template
        context = {'events': events}

        # Render the HTML template with the events data
        return render(request, 'calendar.html', context)
    else:
        return JsonResponse({'message': 'No events found.'})