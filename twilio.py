from twilio.rest import Client

# Your Twilio account SID and auth token
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'

# Create a Twilio client
client = Client(account_sid, auth_token)

# The Twilio phone number from which you want to send the voicemail
twilio_number = '+1234567890'

# The recipient's phone number
recipient_number = '+9876543210'

# URL of the pre-recorded voicemail message
voicemail_url = 'https://example.com/voicemail.mp3'

# Create a call using the Programmable Voice API
call = client.calls.create(
    url=voicemail_url,
    to=recipient_number,
    from_=twilio_number,
    machine_detection='DetectMessageEnd',
    method='GET'
)

print("Voicedrop initiated.")
print("Call SID:", call.sid)