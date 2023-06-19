from twilio.rest import Client
import os

# Twilio setup
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")  # Your Twilio phone number
my_phone_number = os.getenv("MY_PHONE_NUMBER")  # Your personal phone number

client = Client(twilio_account_sid, twilio_auth_token)

def send_order_text(order):
    # Define the message content
    message_content = (
        f"Executed Order!:\n"
        f"Symbol: {order['symbol']}\n"
        f"Quantity: {order['qty']}\n"
        f"Side: {order['side']}\n"
        f"Type: {order['type']}\n"
    )

    message = client.messages.create(
        body=message_content,
        from_=twilio_phone_number,
        to=my_phone_number
    )

    return message.sid


