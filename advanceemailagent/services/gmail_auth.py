

# import os
# import pickle
# import streamlit as st
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build

# SCOPES = [
#     "https://www.googleapis.com/auth/gmail.send",
#     "https://www.googleapis.com/auth/gmail.readonly",
#     "https://www.googleapis.com/auth/gmail.modify",
# ]

# def get_gmail_service():
#     creds = None

#     # Try to load saved token
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)

#     # If no valid creds → new login
#     if not creds or not creds.valid:
#         try:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "client_secret.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)
#             # Save the credentials for next run
#             with open("token.json", "w") as token:
#                 token.write(creds.to_json())
#         except Exception as e:
#             st.error(f"⚠️ Gmail Auth failed: {e}")
#             return None

#     try:
#         service = build("gmail", "v1", credentials=creds)
#         return service
#     except Exception as e:
#         st.error(f"⚠️ Gmail Service failed: {e}")
#         return None


# import os
# import json
# import streamlit as st
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build

# SCOPES = [
#     "https://www.googleapis.com/auth/gmail.send",
#     "https://www.googleapis.com/auth/gmail.readonly",
#     "https://www.googleapis.com/auth/gmail.modify",
# ]

# def get_gmail_service():
#     creds = None

#     # 🔹 Try to load saved token.json (local cache)
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)

#     # 🔹 If no valid creds → login again
#     if not creds or not creds.valid:
#         try:
#             if "gcp" in st.secrets:  
#                 # ✅ Deployment (Streamlit Cloud): use secrets
#                 client_config = json.loads(st.secrets["gcp"]["client_secret"])
#                 flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
#             else:  
#                 # ✅ Local: use client_secret.json file
#                 flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)

#             creds = flow.run_local_server(port=0)

#             # Save creds locally for reuse (only works locally)
#             with open("token.json", "w") as token:
#                 token.write(creds.to_json())

#         except Exception as e:
#             st.error(f"⚠️ Gmail Auth failed: {e}")
#             return None

#     try:
#         service = build("gmail", "v1", credentials=creds)
#         return service
#     except Exception as e:
#         st.error(f"⚠️ Gmail Service failed: {e}")
#         return None




import os
import json
import streamlit as st
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()  # ✅ Local ke liye .env support

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]

def get_gmail_service():
    creds = None

    # 🔹 Try to load saved token.json (local cache)
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 🔹 If no valid creds → login again
    if not creds or not creds.valid:
        try:
            if "gcp" in st.secrets:  
                # ✅ Deployment (Streamlit Cloud)
                client_config = json.loads(st.secrets["gcp"]["client_secret"])
            else:
                # ✅ Local: load from env
                client_config = json.loads(os.getenv("GCP_CLIENT_SECRET"))

            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_console()  

            # Save creds locally for reuse (only works locally)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        except Exception as e:
            st.error(f"⚠️ Gmail Auth failed: {e}")
            return None

    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except Exception as e:
        st.error(f"⚠️ Gmail Service failed: {e}")
        return None

