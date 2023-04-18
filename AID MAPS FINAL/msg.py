from twilio.rest import Client

# Your Twilio account SID and auth token
account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_AUTH_TOKEN'

# Create a Twilio client
client = Client(account_sid, auth_token)

# The number you want to send the message to
to_number = '+91XXXXXXXXX'

# The number your Twilio account is associated with
from_number = '+91XXXXXXXXX'

# The message you want to send
message = 'Hello from Twilio!'

# Send the message using the Twilio API
message = client.messages.create(
    to=to_number, 
    from_=from_number,
    body=message)

# Print the message ID
print(f"Message ID: {message.sid}")
