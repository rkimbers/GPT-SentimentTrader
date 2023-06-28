from twilio.rest import Client
import os

# Twilio setup
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")  
my_phone_number = os.getenv("MY_PHONE_NUMBER")  

client = Client(twilio_account_sid, twilio_auth_token)

def send_order_text(orders):
    # Define the message content
    message_content = "Executed Orders!:\n"

    for order in orders:
        message_content += (
            f"Symbol: {order['symbol']}\n"
            f"Quantity: {order['qty']}\n"
            f"Side: {order['side']}\n"
            f"Type: {order['type']}\n"
            "----------------------\n"
        )

    # Send the message
    message = client.messages.create(
        body=message_content,
        from_=twilio_phone_number,
        to=my_phone_number
    )

    return message.sid

def send_immediate_order_text(order):

    # Construct the message body
    message_body = f"Immediate order submitted!: \n"
    message_body += f"Symbol: {order['symbol']} \n"
    message_body += f"Side: {order['side']} \n"
    message_body += f"Qty: {order['qty']} \n"
    message_body += f"Type: {order['type']} \n"

    # Send the message
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=my_phone_number
    )

    print(f"Sent immediate order message: {message.sid}")