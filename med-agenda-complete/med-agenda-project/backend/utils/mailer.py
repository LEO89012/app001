import os
import aiosmtplib
from email.message import EmailMessage

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
FROM = os.environ.get('SMTP_FROM', SMTP_USER)

async def send_mail(to: str, subject: str, html: str):
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASS:
        # In dev, just print
        print('Mailer not configured. Skipping email to', to)
        return
    msg = EmailMessage()
    msg['From'] = FROM
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(html, subtype='html')
    await aiosmtplib.send(msg, hostname=SMTP_HOST, port=SMTP_PORT, username=SMTP_USER, password=SMTP_PASS, start_tls=True)
