# import os
# import pickle
# import streamlit as st
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from dotenv import load_dotenv

# load_dotenv()

# SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# def get_gmail_service():
#     creds = None
#     if os.path.exists("token.pkl"):
#         with open("token.pkl", "rb") as token:
#             creds = pickle.load(token)

#     if not creds or not creds.valid:
#         try:
#             flow = InstalledAppFlow.from_client_config({
#                 "installed": {
#                     "client_id": os.getenv("GOOGLE_CLIENT_ID"),
#                     "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
#                     "project_id": os.getenv("GOOGLE_PROJECT_ID"),
#                     "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
#                     "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
#                     "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL"),
#                     "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")]
#                 }
#             }, SCOPES)

#             creds = flow.run_local_server(port=0)
#             with open("token.pkl", "wb") as token:
#                 pickle.dump(creds, token)
#         except Exception as e:
#             st.error(f"Gmail Auth failed: {e}")
#             return None

#     try:
#         service = build('gmail', 'v1', credentials=creds)
#         return service
#     except Exception as e:
#         st.error(f"Gmail Service failed: {e}")
#         return None



import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Gmail send and read access
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send"
]

def get_gmail_service():
    creds = None
    token_path = "token.pkl"

    # Token file exists
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    # Token invalid or expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save token
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    try:
        # Build Gmail service
        service = build("gmail", "v1", credentials=creds)
        return service
    except Exception as e:
        print(f"❌ Failed to create Gmail service: {e}")
        return None
