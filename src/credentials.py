import os
import logging
import pickle
from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow


logger = logging.getLogger(__name__)
secrets_path = "../secrets/"


def get_credentials():
    pickle_file = os.path.join(secrets_path, "token.pickle")
    credentials = None

    # Token is saved on disk
    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as token:
            credentials = pickle.load(token)
            print("Credentials loaded from disk")
        # If credentials is expired, we need to renew it
        if credentials.expired and credentials.refresh_token:
            mes = "Credentials Expired, refreshing"
            print(mes)
            logger.debug(mes)
            try:
                credentials.refresh(Request())
                mes = "Credentials refreshed"
                print(mes)
                logger.debug(mes)
            except Exception as e:
                mes = f"{e} Failed to refresh credentials, obtaining new ones"
                print(mes)
                logger.debug(mes)
                credentials = _get_new_credentials()

    # Token is not saved on disk
    else:
        # Obtain new token
        mes = "Credentials don't exist, requesting new tokens"
        print(mes)
        logger.debug(mes)
        credentials = _get_new_credentials()
    # Always save token back to disk
    with open(pickle_file, "wb") as token:
        pickle.dump(credentials, token)
    return credentials


def _get_new_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(secrets_path, "client_secret.json"),
        scopes=["https://www.googleapis.com/auth/sdm.service"],
    )
    flow.run_local_server()
    return flow.credentials
