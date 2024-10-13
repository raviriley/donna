from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import os
import requests


def get_twilio_client() -> TwilioClient:
    load_dotenv()
    account_sid: str = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token: str = os.environ.get("TWILIO_AUTH_TOKEN")
    return TwilioClient(account_sid, auth_token)


def send_text_message(to_number: str, message_body: str, from_number: str) -> str:
    """Sends a text message using Twilio."""
    twilio_client = get_twilio_client()
    message = twilio_client.messages.create(
        body=message_body, from_=from_number, to=to_number
    )
    print(f"Message sent! Message SID: {message.sid}")
    return message.sid


def get_caller_number(call_sid: str) -> str:
    # Twilio API base URL
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    base_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Calls/{call_sid}.json"
    auth_header = (account_sid, auth_token)
    response = requests.get(base_url, auth=auth_header)
    if response.status_code == 200:
        to = response.json()["to"]
        from_number = response.json()["from"]
        # check if the number is the dart number
        if to == os.environ.get("TWILIO_PHONE_NUMBER"):
            return from_number
        else:
            return to
    else:
        return ""


def transfer_call(call_sid: str, new_phone_number: str) -> None:
    """Transfers an existing call to a different phone number mid-stream."""
    twiml_response = f"""<Response>
                <Dial>{new_phone_number}</Dial>
            </Response>"""
    twilio_client = get_twilio_client()
    twilio_client.calls(call_sid).update(twiml=twiml_response)
    print(f"Call transferred to {new_phone_number} with Call SID: {call_sid}")


def end_call(call_sid: str) -> None:
    """Ends an ongoing Twilio call."""
    twilio_client = get_twilio_client()
    try:
        twilio_client.calls(call_sid).update(status="completed")
        print(f"Call with SID {call_sid} has been ended.")
    except Exception as e:
        print(f"Error ending call with SID {call_sid}: {str(e)}")


def schedule_call(phone_number: str) -> None:
    print(f"Scheduling for {phone_number}")
    # send sms to phone number with link to calendar
    message = f"Please schedule a call with Harvey at {os.environ.get('CALENDLY_URL')}"
    TWILIO_PHONE_NUMBER: str = os.environ.get("TWILIO_PHONE_NUMBER")
    send_text_message(phone_number, message, TWILIO_PHONE_NUMBER)
