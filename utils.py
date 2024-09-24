from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
load_dotenv()

SHEET_ID = os.environ.get("SHEET_ID")


def authenticate_sheets():
    credentials = None

    if os.path.exists("token.json"):
        try:
            credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
        except:
            pass
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("token.json", SCOPES)
            credentials = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(credentials.to_json())

    return build("sheets", "v4", credentials=credentials)


def write_sheet(values):
    sheets = authenticate_sheets()
    body = {"values": values}

    result = (
        sheets.spreadsheets()
        .values()
        .append(
            spreadsheetId=SHEET_ID,
            range="Sheet1",
            valueInputOption="RAW",
            body=body,
            insertDataOption="INSERT_ROWS",
        )
        .execute()
    )

    return result
