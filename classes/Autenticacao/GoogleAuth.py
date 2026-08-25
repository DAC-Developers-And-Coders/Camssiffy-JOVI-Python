import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class GoogleAuth:
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    ARQUIVO_CREDENCIAIS = "credentials.json"
    ARQUIVO_TOKEN = "token.json"

    @classmethod
    def autenticar(cls):
        creds = None

        if os.path.exists(cls.ARQUIVO_TOKEN):
            creds = Credentials.from_authorized_user_file(cls.ARQUIVO_TOKEN, cls.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(cls.ARQUIVO_CREDENCIAIS, cls.SCOPES)
                creds = flow.run_local_server(port=0)

            with open(cls.ARQUIVO_TOKEN, "w") as token:
                token.write(creds.to_json())

        return creds