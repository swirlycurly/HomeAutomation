import os
import pickle
from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow


def get_credentials():
    pickle_file = './secrets/token.pickle'
    credentials = None

    # Token is saved on disk
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            credentials = pickle.load(token)
            print("Credentials loaded from disk")
        # If credentials is expired, we need to renew it
        if credentials.expired and credentials.refresh_token:
            print("Credentials Expired, refreshing")
            credentials.refresh(Request())
            print("Credentails refreshed")
    # Token is not saved on disk
    else:
        # Obtain new token
        print("Credentials don't exist, requesting new tokens")
        flow = InstalledAppFlow.from_client_secrets_file(
                './secrets/client_secret.json',
                scopes=['https://www.googleapis.com/auth/sdm.service'])
        flow.run_local_server()
        credentials = flow.credentials
    # Always save token back to disk
    with open(pickle_file, 'wb') as token:
        pickle.dump(credentials, token)
    return credentials
