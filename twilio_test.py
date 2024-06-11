import json
import re
from twilio.rest import Client

def is_valid_phone_number(phone_number):
    # Check if the phone number is in E.164 format
    pattern = re.compile(r'^\+\d{1,15}$')
    return pattern.match(phone_number)

def send_reservation_text(cur_reservation):
    # Load credentials from accounts.json
    with open('accounts.json', 'r') as file:
        data = json.load(file)

    account_sid = data["account_sid"]
    auth_token = data["auth_token"]
    twilio_number = data["twilio_number"]
    to_phone_numbers = data["to_phone_number"]


    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Create the message
    message_body = f"This is Twilio. Reservations are now available at {cur_reservation}"

    # Send the message to all numbers in the list
    for number in to_phone_numbers:
        if is_valid_phone_number(number):
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=number
            )
            print(f"Message sent to {number}: {message.sid}")
        else:
            print(f"Invalid phone number: {number}")

# Example usage
send_reservation_text("Ohana at Disney World")
