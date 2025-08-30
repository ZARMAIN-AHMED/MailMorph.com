from email.mime.text import MIMEText
import base64

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_email(service, user_id, message):
    return service.users().messages().send(userId=user_id, body=message).execute()
