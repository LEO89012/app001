import os
from twilio.rest import Client

TW_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TW_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TW_FROM = os.environ.get('TWILIO_FROM_PHONE')  # e.g. +1415...
client = None
if TW_SID and TW_TOKEN:
    client = Client(TW_SID, TW_TOKEN)

def send_whatsapp(to_number: str, body: str):
    if not client:
        print('Twilio not configured. Skipping WhatsApp to', to_number)
        return None
    return client.messages.create(body=body, from_=TW_FROM, to=to_number)
