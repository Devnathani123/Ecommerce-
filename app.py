from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# Load your service account JSON key file
SERVICE_ACCOUNT_FILE = 'outh.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Create a Google Sheets API client
service = build('sheets', 'v4', credentials=creds)
sheet_id = '19_3Ldqq-RkgXXtqp3LM45TsTNaX2SC6sYpMTnmVZJJg'

@app.route('/read_sheet')
def read_sheet():
    # Specify range in the format "Sheet1!A1:D10"
    range_name = 'Sheet1!A1:D10'
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])
    return jsonify(values)

@app.route('/write_sheet')
def write_sheet():
    # Specify the range and data to write
    range_name = 'Sheet1!A2'
    values = [["Hello", "World"]]
    body = {'values': values}
    sheet = service.spreadsheets()
    result = sheet.values().update(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption='RAW', body=body
    ).execute()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
