import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import sys

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'service-account.json'

def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_file(file_path, folder_id=None):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File uploaded: {file_metadata}, to {file}')
    print(f'File ID: {file.get("id")}')

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: python upload.py <file_path> [<folder_id>]")
        sys.exit(1)

    file_path = sys.argv[1]
    folder_id = sys.argv[2]
    upload_file(file_path, folder_id)
