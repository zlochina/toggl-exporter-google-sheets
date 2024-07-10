import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def load_google_config(config):
    return config["Google"]["spreadsheet_id"], config["Google"]["range"]


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

        # First, get the current data in the sheet
        result = (
            sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        )
        current_values = result.get("values", [])

        # If the sheet is empty, add headers
        if not current_values:
            headers = [
                "Date",
                "Time (Finished at)",
                "Duration(Hours)",
                "Task",
                "Description",
            ]
            sheet.values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body={"values": [headers]},
            ).execute()

        # Prepare the new data
        new_values = []
        for row in data:
            # Check if this row already exists in the sheet
            if row not in current_values:
                new_values.append(row)

        if new_values:
            # Append only new rows
            result = (
                sheet.values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption="USER_ENTERED",
                    body={"values": new_values},
                )
                .execute()
            )
            print(f"{result.get('updates').get('updatedRows')} rows appended.")
        else:
            print("No new data to append.")

    except HttpError as error:
        print(f"An error occurred: {error}")
