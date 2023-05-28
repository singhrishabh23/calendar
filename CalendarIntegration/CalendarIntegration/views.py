from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.views import View
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class GoogleCalendarInitView(View):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        return redirect(auth_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        flow.fetch_token(
            authorization_response=request.get_full_path(),
            redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
        )

        credentials = flow.credentials
        if not credentials.valid:
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                return redirect('/error/')  # Handle the error condition appropriately

        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        # Process the events as per your requirement

        return redirect('/success/')  # Redirect to a success page or return JSON response

