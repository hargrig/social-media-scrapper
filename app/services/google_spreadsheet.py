import os
import gspread

from typing import Any
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSpreadsheetService:
    def __init__(self, spreadsheet_data: Any, header: list = []):
        self.client = None
        self.header = header
        self.spreadsheet_data = spreadsheet_data

    def init_qcp_client(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        base_dir = os.path.dirname(os.path.abspath(__file__))
        creds_path = os.path.join(base_dir, '..', 'config', 'gcp-creds.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)

        # Authorize the clientsheet 
        client = gspread.authorize(creds)
        self.client = client

    def fill_spreadsheet(self):
        self.init_qcp_client()

        spreadsheet = self.client.open("InternalSocialMedias")
        worksheets_obj = spreadsheet.worksheets()

        worksheets = [ 
            worksheet.title for worksheet in worksheets_obj 
        ]

        for worksheet, worksheet_row_data in self.spreadsheet_data.items():
            if worksheet not in worksheets:
                print(f"Please add worksheet {worksheet} in spreadshet file")
                continue

            worksheet = spreadsheet.worksheet(worksheet)
            worksheet.append_row(worksheet_row_data)
