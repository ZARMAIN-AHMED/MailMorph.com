# services/email_storage.py
import json
import os

STORAGE_FILE = "sent_emails.json"

def save_email(entry):
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_emails():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    return []