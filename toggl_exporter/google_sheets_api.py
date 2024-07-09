import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def load_google_config(config):
    return config["Google"]["spreadsheet_id"]


def get_google_sheets_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("sheets", "v4", credentials=creds)


def export_to_google_sheets(data, spreadsheet_id, range_name):
    try:
        service = get_google_sheets_service()
        sheet = service.spreadsheets()

        # Clear existing content
        sheet.values().clear(spreadsheetId=spreadsheet_id, range=range_name).execute()

        # Prepare the data with headers
        values = [
            ["Date", "Time (Finished at)", "Duration(Hours)", "Task", "Description"]
        ] + data

        body = {"values": values}
        result = (
            sheet.values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
    except HttpError as error:
        print(f"An error occurred: {error}")
