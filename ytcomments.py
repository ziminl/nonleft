##pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client



import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def get_authenticated_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

def delete_all_comments(service):
    request = service.commentThreads().list(
        part='id',
        myRecentComments=True,
        maxResults=100
    )
    response = request.execute()
    
    while response:
        for item in response['items']:
            comment_id = item['id']
            try:
                service.comments().delete(id=comment_id).execute()
                print(f'Deleted comment: {comment_id}')
            except Exception as e:
                print(f'An error occurred: {e}')
        
        if 'nextPageToken' in response:
            request = service.commentThreads().list(
                part='id',
                myRecentComments=True,
                maxResults=100,
                pageToken=response['nextPageToken']
            )
            response = request.execute()
        else:
            break

if __name__ == '__main__':
    service = get_authenticated_service()
    delete_all_comments(service)


