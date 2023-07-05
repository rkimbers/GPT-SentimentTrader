from twilio.rest import Client
import concurrent.futures
import os

def create_twilio_client():
    twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(twilio_account_sid, twilio_auth_token)
    #client.http_client.debug = True  # turn on debug mode
    return client


def send_order_text(orders):
    try:
        client = create_twilio_client()

        twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")  
        my_phone_number = os.getenv("MY_PHONE_NUMBER")  

        # Define the message content
        message_content = "Executed Orders!:\n"

        for order in orders:
            order_text = (
                f"Symbol: {order['symbol']}\n"
                f"Quantity: {order['qty']}\n"
                f"Side: {order['side']}\n"
                f"Type: {order['type']}\n"
                "----------------------\n"
            )

            # Check if adding the next order would exceed the limit
            if len(message_content) + len(order_text) > 1600:
                # If it would, send the current message content
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(client.messages.create, body=message_content, from_=twilio_phone_number, to=my_phone_number)
                    try:
                        future.result(timeout=10)  # 10 seconds timeout
                    except concurrent.futures.TimeoutError:
                        print('SMS sending timed out')
                # Start a new message content with the current order
                message_content = "Executed Orders!:\n" + order_text
            else:
                # If it wouldn't, add the order to the current message content
                message_content += order_text

        # Send the remaining message content
        if message_content.strip() != "Executed Orders!:":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(client.messages.create, body=message_content, from_=twilio_phone_number, to=my_phone_number)
                try:
                    future.result(timeout=10)  # 10 seconds timeout
                except concurrent.futures.TimeoutError:
                    print('SMS sending timed out')

    except Exception as e:
        print(f"Failed to send message: {e}")


def send_immediate_order_text(order):
    try:
        client = create_twilio_client()

        twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")  
        my_phone_number = os.getenv("MY_PHONE_NUMBER")  

        # Define the message content
        message_content = "Immediate order submitted!:\n"
        
        order_text = (
            f"Symbol: {order['symbol']}\n"
            f"Quantity: {order['qty']}\n"
            f"Side: {order['side']}\n"
            f"Type: {order['type']}\n"
            "----------------------\n"
        )

        # Check if adding the order would exceed the limit
        if len(message_content) + len(order_text) > 1600:
            # If it would, send the current message content
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(client.messages.create, body=message_content, from_=twilio_phone_number, to=my_phone_number)
                try:
                    future.result(timeout=10)  # 10 seconds timeout
                except concurrent.futures.TimeoutError:
                    print('SMS sending timed out')
            # Start a new message content with the order
            message_content = "Immediate order submitted!:\n" + order_text
        else:
            # If it wouldn't, add the order to the message content
            message_content += order_text

        # Send the remaining message content
        if message_content.strip() != "Immediate order submitted!:":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(client.messages.create, body=message_content, from_=twilio_phone_number, to=my_phone_number)
                try:
                    future.result(timeout=10)  # 10 seconds timeout
                except concurrent.futures.TimeoutError:
                    print('SMS sending timed out')

    except Exception as e:
        print(f"Failed to send message: {e}")
