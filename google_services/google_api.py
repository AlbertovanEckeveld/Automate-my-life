import os.path

from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE')

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def get_credentials():
    """Gets user credentials for Gmail and Calendar API"""
    creds = None
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE or not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError("Credentials file not found. Check your .env configuration.")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_gmail_service():
    """Returns Gmail API service"""
    creds = get_credentials()
    return build('gmail', 'v1', credentials=creds)

def get_calendar_service():
    """Returns Google Calendar API service"""
    creds = get_credentials()
    return build('calendar', 'v3', credentials=creds)
