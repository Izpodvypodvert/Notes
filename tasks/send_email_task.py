import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

from celery import Celery


load_dotenv()
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
REDIS_URL = os.environ.get('REDIS_URL')

celery = Celery('tasks', broker={REDIS_URL})


@celery.task
def send_email_with_notes(user: dict):
    email = get_email_template(user)
    if SMTP_USER is not None and SMTP_PASSWORD is not None:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(email)
    else:
        raise ValueError("SMTP credentials are not set")


def get_email_template(user: dict):
    email = EmailMessage()
    email['Subject'] = 'Ваши заметки'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER
    html_content = create_html_content_for_user(user)
    email.set_content(
        html_content,
        subtype='html'
    )
    return email


def create_html_content_for_user(user: dict) -> str:
    username = user["email"].split("@")[0]
    html_content = f'<div><h1 style="color: red;">Здравствуйте, {
        username}. Ваши заметки 📝.</h1><ul>'
    for note in user["notes"]:
        html_content += f'<li><strong>{note["title"]
                                       }</strong>: {note["description"]}</li>'
    html_content += '</ul></div>'
    return html_content
