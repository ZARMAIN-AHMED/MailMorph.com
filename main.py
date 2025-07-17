import streamlit as st
from services.gmail_auth import get_gmail_service
from services.ai_writer import generate_email
from email.mime.text import MIMEText
import base64

st.set_page_config(page_title="📧 Cold Email Closer", layout="centered")
st.title("📧 Cold Email Closer (AI Powered)")

if "gmail_service" not in st.session_state:
    st.session_state.gmail_service = None
if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""
if "email_ready_to_send" not in st.session_state:
    st.session_state.email_ready_to_send = False

# Step 1: Gmail login
st.header("Step 1: Gmail Login")
if st.button("🔐 Login to Gmail"):
    service = get_gmail_service()
    if service:
        st.success("✅ Logged in to Gmail")
        st.session_state.gmail_service = service
    else:
        st.error("❌ Login failed")

# Step 2: Get lead info
st.header("Step 2: Enter Lead Info")
to_email = st.text_input("Recipient Email")
company = st.text_input("Company Name")
service = st.text_area("Describe your service", height=100)

# Step 3: Generate Email
st.header("Step 3: Generate Cold Email")
if st.session_state.gmail_service and st.button("📝 Generate Email"):
    if not (to_email and company and service):
        st.warning("⚠️ Please fill all fields.")
    else:
        with st.spinner("🤖 Generating email..."):
            email_body = generate_email(company, service)
            if not email_body:
                st.error("❌ AI failed to generate email.")
            else:
                st.success("✅ Email generated!")
                st.session_state.generated_email = email_body
                st.session_state.email_ready_to_send = True

# Show editable email if generated
if st.session_state.email_ready_to_send:
    st.header("Step 4: Edit & Send Email")
    edited_email = st.text_area("✏️ Edit your email before sending", st.session_state.generated_email, height=200)

    if st.button("📤 Send Email"):
        message = MIMEText(edited_email)
        message['to'] = to_email
        message['subject'] = f"Quick Note from {company}"
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            st.session_state.gmail_service.users().messages().send(
                userId="me", body={'raw': raw}
            ).execute()
            st.success("✅ Email sent successfully!")
            st.session_state.email_ready_to_send = False
            st.session_state.generated_email = ""
        except Exception as e:
            st.error(f"❌ Failed to send: {e}")
