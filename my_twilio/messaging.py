# file: my_twilio/messaging.py
from twilio.rest import Client
import concurrent.futures
import os
import logging


def create_twilio_client():
    twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    try:
        client = Client(twilio_account_sid, twilio_auth_token)
        return client
    except Exception as e:
        logging.error(f"Failed to create Twilio client: {e}")

def send_order_text(orders):
    try:
        client = create_twilio_client()
        twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")  
        my_phone_number = os.getenv("MY_PHONE_NUMBER")  

        message_content = "Executed Orders!:\n"

        for order in orders:
            order_text = (
                f"Symbol: {order['symbol']}\n"
                f"Quantity: {order['qty']}\n"
                f"Side: {order['side']}\n"
                f"Type: {order['type']}\n"
                "----------------------\n"
            )

            if len(message_content) + len(order_text) > 1600:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(client.messages.create, body=message_content, from_=twilio_phone_number, to=my_phone_number)
                    try:
                        future.result(timeout=10)
                    except concurrent.futures.TimeoutError:
                        logging.error('SMS sending timed out')
                message_content = "Executed Orders!:\n" + order_text
            else:
                message_content += order_text

        if message_content.strip() != "Executed Orders!:":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(client.messages.create, body=message_content, from_=twilio_phone_number, to=my_phone_number)
                try:
                    future.result(timeout=10)
                except concurrent.futures.TimeoutError:
                    logging.error('SMS sending timed out')

    except Exception as e:
        logging.error(f"Failed to send message: {e}")

def send_immediate_order_text(order):
    try:
        client = create_twilio_client()

        twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")  
        my_phone_number = os.getenv("MY_PHONE_NUMBER")  

        message_content = "Immediate order submitted!:\n"
        
        order_text = (
            f"Symbol: {order['symbol']}\n"
            f"Quantity: {order['qty']}\n"
            f"Side: {order['side']}\n"
            f"Type: {order['type']}\n"
            "----------------------\n"
        )

        if len(message_content) + len(order_text) > 1600:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(client.messages.create, body=message_content, from_=twilio_phone_number, to=my_phone_number)
                try:
                    future.result(timeout=10)
                except concurrent.futures.TimeoutError:
                    logging.error('SMS sending timed out')
            message_content = "Immediate order submitted!:\n" + order_text
        else:
            message_content += order_text

        if message_content.strip() != "Immediate order submitted!:":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(client.messages.create, body=message_content, from_=twilio_phone_number, to=my_phone_number)
                try:
                    future.result(timeout=10)
                except concurrent.futures.TimeoutError:
                    logging.error('SMS sending timed out')

    except Exception as e:
        logging.error(f"Failed to send message: {e}")

def send_market_open_message(status, error=None):
    try:
        client = create_twilio_client()

        twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        my_phone_number = os.getenv("MY_PHONE_NUMBER")

        if status == "no_trades":
            message_content = "No trades were executed today at market open."
        elif status == "trades_executed":
            message_content = "Trades were executed today at market open."
        else:
            message_content = f"An error occurred at market open: {error}"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(client.messages.create, body=message_content, from_=twilio_phone_number, to=my_phone_number)
            try:
                future.result(timeout=10)
            except concurrent.futures.TimeoutError:
                logging.error('SMS sending timed out')

    except Exception as e:
        logging.error(f"Failed to send market open message: {e}")
