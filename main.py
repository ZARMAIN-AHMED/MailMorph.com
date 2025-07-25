# import streamlit as st
# from services.gmail_auth import get_gmail_service
# from services.ai_writer import generate_email
# from email.mime.text import MIMEText
# import base64

# st.set_page_config(page_title="📧 Cold Email Closer", layout="centered")
# st.title("📧 Cold Email Closer (AI Powered)")

# if "gmail_service" not in st.session_state:
#     st.session_state.gmail_service = None
# if "generated_email" not in st.session_state:
#     st.session_state.generated_email = ""
# if "email_ready_to_send" not in st.session_state:
#     st.session_state.email_ready_to_send = False

# # Step 1: Gmail login
# st.header("Step 1: Gmail Login")
# if st.button("🔐 Login to Gmail"):
#     service = get_gmail_service()
#     if service:
#         st.success("✅ Logged in to Gmail")
#         st.session_state.gmail_service = service
#     else:
#         st.error("❌ Login failed")

# # Step 2: Get lead info
# st.header("Step 2: Enter Lead Info")
# to_email = st.text_input("Recipient Email")
# company = st.text_input("Company Name")
# service = st.text_area("Describe your service", height=100)

# # Step 3: Generate Email
# st.header("Step 3: Generate Cold Email")
# if st.session_state.gmail_service and st.button("📝 Generate Email"):
#     if not (to_email and company and service):
#         st.warning("⚠️ Please fill all fields.")
#     else:
#         with st.spinner("🤖 Generating email..."):
#             email_body = generate_email(company, service)
#             if not email_body:
#                 st.error("❌ AI failed to generate email.")
#             else:
#                 st.success("✅ Email generated!")
#                 st.session_state.generated_email = email_body
#                 st.session_state.email_ready_to_send = True

# # Show editable email if generated
# if st.session_state.email_ready_to_send:
#     st.header("Step 4: Edit & Send Email")
#     edited_email = st.text_area("✏️ Edit your email before sending", st.session_state.generated_email, height=200)

#     if st.button("📤 Send Email"):
#         message = MIMEText(edited_email)
#         message['to'] = to_email
#         message['subject'] = f"Quick Note from {company}"
#         raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

#         try:
#             st.session_state.gmail_service.users().messages().send(
#                 userId="me", body={'raw': raw}
#             ).execute()
#             st.success("✅ Email sent successfully!")
#             st.session_state.email_ready_to_send = False
#             st.session_state.generated_email = ""
#         except Exception as e:
#             st.error(f"❌ Failed to send: {e}")



import streamlit as st
import json
import base64
import os
import asyncio
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
from services.gmail_auth import get_gmail_service
from services.ai_writer import generate_email  # یہ async ہونا چاہیے

st.set_page_config(page_title="AI Cold Emailer", layout="wide")
st.title("📨 AI Cold Emailer with Reply Tracker")

# --- Session state ---
if "gmail_service" not in st.session_state:
    st.session_state.gmail_service = None
if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

# --- Step 1: Login to Gmail ---
st.subheader("🔐 Step 1: Login to Gmail")
if st.button("🔑 Login to Gmail"):
    service = get_gmail_service()
    if service:
        st.session_state.gmail_service = service
        st.success("✅ Logged in successfully!")
    else:
        st.error("❌ Login failed.")

if not st.session_state.gmail_service:
    st.warning("⚠️ Please login to continue.")
    st.stop()

service = st.session_state.gmail_service

# --- File to track sent emails ---
EMAILS_FILE = "sent_emails.json"

def load_sent_emails():
    if os.path.exists(EMAILS_FILE):
        with open(EMAILS_FILE, "r") as f:
            return json.load(f)
    return []

def save_sent_email(email):
    emails = load_sent_emails()
    emails.append(email)
    with open(EMAILS_FILE, "w") as f:
        json.dump(emails, f, indent=2)

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}

def send_email(to, subject, body):
    try:
        message = create_message(to, subject, body)
        sent = service.users().messages().send(userId="me", body=message).execute()
        thread_id = sent["threadId"]
        save_sent_email({"to": to, "subject": subject, "body": body, "threadId": thread_id})
        st.success("✅ Email sent successfully!")
    except HttpError as error:
        st.error(f"❌ Failed to send email: {error}")

def get_thread_messages(thread_id):
    try:
        thread = service.users().threads().get(userId="me", id=thread_id).execute()
        return thread["messages"]
    except Exception as e:
        st.error(f"❌ Error fetching thread: {e}")
        return []

def reply_to_thread(thread_id, to, body):
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = "Re:"
    message["In-Reply-To"] = thread_id
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    reply_body = {"raw": raw, "threadId": thread_id}
    try:
        service.users().messages().send(userId="me", body=reply_body).execute()
        st.success("✅ Reply sent!")
    except HttpError as error:
        st.error(f"❌ Failed to reply: {error}")

# --- Step 2: Generate + Compose + Send ---
st.subheader("✍️ Step 2: Generate and Send Cold Email")

with st.form("generate_email_form"):
    to = st.text_input("Recipient Email")
    company = st.text_input("🏢 Company Name")
    service_offer = st.text_area("🛠️ Your Service / Offer")
    generate = st.form_submit_button("✨ Generate Email")

    if generate:
        if not to or not company or not service_offer:
            st.warning("⚠️ Please fill all fields.")
        else:
            with st.spinner("Generating email..."):
                try:
                    generated = asyncio.run(generate_email(company, service_offer))
                    st.session_state.generated_email = generated
                    st.session_state.to = to
                    st.session_state.subject = f"Cold Email to {company}"
                    st.success("✅ Email generated!")
                except Exception as e:
                    st.error(f"❌ Error generating email: {e}")

# --- Show generated email preview ---
if st.session_state.generated_email:
    st.markdown("#### ✉️ Generated Email Preview (Editable)")
    edited_body = st.text_area("Email Body", value=st.session_state.generated_email, height=200)

    if st.button("📤 Send Email"):
        if not st.session_state.to or not edited_body:
            st.warning("⚠️ Missing required info.")
        else:
            send_email(st.session_state.to, st.session_state.subject, edited_body)
            st.session_state.generated_email = ""
            st.session_state.to = ""
            st.session_state.subject = ""

# --- Step 3: View Sent Emails and Replies ---
st.subheader("📬 Sent Emails & Replies")

sent_emails = load_sent_emails()
if not sent_emails:
    st.info("No emails sent yet.")
else:
    for idx, email in enumerate(reversed(sent_emails)):
        with st.expander(f"📨 {email['subject']} → {email['to']}"):
            st.markdown(f"**To:** {email['to']}")
            st.markdown(f"**Subject:** {email['subject']}")
            st.markdown(f"**Message:**\n\n{email['body']}")

            messages = get_thread_messages(email["threadId"])
            replies = [m for m in messages if "labelIds" in m and "INBOX" in m["labelIds"]]
            if replies:
                st.markdown("---")
                st.markdown("**📥 Replies:**")
                for r in replies:
                    headers = r["payload"]["headers"]
                    from_email = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
                    snippet = r.get("snippet", "")
                    st.markdown(f"**{from_email}**: {snippet}")

            with st.form(f"reply_form_{idx}"):
                reply_msg = st.text_area("💬 Write your reply", key=f"reply_input_{idx}")
                send_reply = st.form_submit_button("↩️ Send Reply")
                if send_reply:
                    reply_to_thread(email["threadId"], email["to"], reply_msg)
