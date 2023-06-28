# my_twilio

The `my_twilio` directory contains modules related to sms messaging with the Twilio API. The main component is `messaging.py`.

## Files

### messaging.py

This file contains the functions to send sms messages to the personal phone number from the twilio phone number definited as an environment variable. It contains 2 functions that carry the same purpose and are structured similarly. 

#### `send_order_text()`
Both `send_order_text()` and `send_immediate_order_text()` send messages containing the same content: the order ticker, quantity, side, and order type. `send_order_text()` is designed to send a single large message containing multiple orders depending on the order's side, where all buy orders are grouped together and all sell orders are grouped together. 

#### `send_immediate_order_text()`
This function acts the same as `send_order_text()` but will only send one order per message, as it is called each time that an immediate order is placed.

## Usage

Import the necessary functions from each file as needed. For example, to use the `send_order_text()` function in your code, you would use:

```python
from my_twilio.messaging import send_order_text