from .main import get_twilio_client

def send_text_message(to_number: str, message_body: str, from_number: str) -> str:
    """Sends a text message using Twilio."""
    twilio_client = get_twilio_client()
    message = twilio_client.messages.create(
        body=message_body,
        from_=from_number,
        to=to_number
    )
    print(f"Message sent! Message SID: {message.sid}")
    return message.sid