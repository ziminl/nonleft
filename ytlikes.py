## enable ytapi permissions: ensure that your OAuth 2.0 Client ID has the necessary permissions to modify your playlists


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
    # Token file to store the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

# Function to delete all likes (remove liked videos from the 'Liked videos' playlist)
def delete_all_likes(service):
    liked_videos_playlist_id = 'LL'  # The playlist ID for 'Liked videos'

    # Get all liked videos
    request = service.playlistItems().list(
        part='id,snippet',
        playlistId=liked_videos_playlist_id,
        maxResults=50
    )
    response = request.execute()
    
    while response:
        for item in response['items']:
            video_id = item['id']
            try:
                service.playlistItems().delete(id=video_id).execute()
                print(f'Removed like from video: {video_id}')
            except Exception as e:
                print(f'An error occurred: {e}')
        
        if 'nextPageToken' in response:
            request = service.playlistItems().list(
                part='id,snippet',
                playlistId=liked_videos_playlist_id,
                maxResults=50,
                pageToken=response['nextPageToken']
            )
            response = request.execute()
        else:
            break

if __name__ == '__main__':
    service = get_authenticated_service()
    delete_all_likes(service)



