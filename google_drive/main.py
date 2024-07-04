import os
import sys

# Add parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from fastapi.responses import JSONResponse
import os
import io
from googleapiclient.errors import HttpError

scope = ['https://www.googleapis.com/auth/drive']
service_account_json_key = 'google_drive/credentials.json'
credentials = service_account.Credentials.from_service_account_file(
                              filename=service_account_json_key,
                              scopes=scope)
service = build('drive', 'v3', credentials=credentials)

def is_valid_format(file_name: str,VALID_FORMATS:list) -> bool:
    _, file_extension = os.path.splitext(file_name)
    return file_extension.lower()[1:] in VALID_FORMATS
def upload_file_to_drive(file_path, folder_name,VALID_FORMATS:list=['jpg', 'jpeg', 'png']):
    if not is_valid_format(os.path.basename(file_path),VALID_FORMATS):
        return None  # Invalid format
    # Get the ID of the target folder
    folder_query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=folder_query).execute()
    folder_id = results.get('files', [])[0]['id'] if results.get('files', []) else None

    # If the folder doesn't exist, create it
    if not folder_id:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')

    # Create a media file upload instance with the file path and MIME type
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')

    # Define the file metadata, including the file name and parent folder ID
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }

    try:
        # Upload the file to Google Drive
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Get the file ID
        file_id = file.get('id')

        # Define the permission for the file (make it publicly accessible)
        permission_metadata = {
            'role': 'reader',
            'type': 'anyone'
        }

        # Create the permission for the file
        permission = service.permissions().create(fileId=file_id, body=permission_metadata).execute()

        # Get the URL of the file
        file_url = f"https://drive.google.com/uc?id={file_id}"
        return file_url
    except Exception as error:
        print('An error occurred: %s' % error)
        return ""



    
if __name__=="__main__":
   print(upload_file_to_drive("docs/api-image.png","pubai",['jpg', 'jpeg', 'png']))
   