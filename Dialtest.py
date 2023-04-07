# Install the twilio library first: pip install twilio
from twilio.rest import Client

# Your Twilio account SID and authentication token
account_sid = 'id'
auth_token = 'token'

# Create a Twilio client object
client = Client(account_sid, auth_token)

# The phone number to call
to_phone_number = '+91xxxxxxxxxx'  # Replace with the number you want to call

# The Twilio phone number to use as the caller ID
from_phone_number = 'ph0_no'  # Replace with your Twilio phone number

# Make the call
call = client.calls.create(
    to=to_phone_number,
    from_=from_phone_number,
    url='http://demo.twilio.com/docs/voice.xml'  # Replace with the URL of your TwiML script
)

print('Call SID:', call.sid)  # Print the unique ID of the call
