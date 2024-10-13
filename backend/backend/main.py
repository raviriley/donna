from fastapi import Depends, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi import FastAPI
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import os
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
import websockets
from .utils import (
    get_twilio_client,
    transfer_call,
    schedule_call,
    get_caller_number,
    end_call,
)
from .google_functions import get_events_for_today

app = FastAPI()


class CallRequest(BaseModel):
    phone_number: str = Field(..., description="The phone number to call")


@app.post("/calls/outbound")
async def trigger_outbound_call(
    request: CallRequest,
    twilio_client: TwilioClient = Depends(get_twilio_client),
) -> JSONResponse:
    phone_number = request.phone_number

    TWILIO_PHONE_NUMBER: str = os.environ.get("TWILIO_PHONE_NUMBER")
    STREAM_URL: str = os.environ.get("STREAM_URL")

    twiml_response = f"""<Response>
                <Connect>
                    <Stream url="{STREAM_URL}">
                    </Stream>
                </Connect>
                <Pause length='1'/>
            </Response>"""

    call = twilio_client.calls.create(
        twiml=twiml_response,
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
    )

    print(f"Call initiated! Call SID: {call.sid}")

    return JSONResponse(
        status_code=200,
        content={
            "message": f"Call initiated! Call SID: {call.sid}",
            "twilio_call_sid": call.sid,
        },
    )

@app.post("/calls/inbound")
async def handle_inbound_call(
    request: Request,
    twilio_client: TwilioClient = Depends(get_twilio_client),
) -> Response:
    """Handles an inbound call from Twilio."""
    STREAM_URL: str = os.environ.get("STREAM_URL")
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    from_number = form_data.get("From")
    to_number = form_data.get("To")

    print(f"Incoming call from {from_number} to {to_number} with Call SID: {call_sid}")

    # Generate TwiML response to handle the call
    twiml_response = f"""<Response>
                <Connect>
                    <Stream url="{STREAM_URL}">
                    </Stream>
                </Connect>
            </Response>"""

    content_type = "application/xml"

    # Return a Response object with the TwiML response and content type
    return Response(content=twiml_response, media_type=content_type)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    call_sid = None  # Initialize call_sid to store the call ID
    stream_sid = None
    # Load environment variables
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    link_sent = False

    # Connect to OpenAI Realtime API
    async with websockets.connect(
        "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01",
        extra_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1",
        },
    ) as openai_ws:
        # Send session update with system prompt
        await send_session_update(openai_ws)

        async def receive_from_twilio() -> None:
            nonlocal call_sid
            nonlocal stream_sid
            try:
                while True:
                    data = await websocket.receive_text()
                    data_json = json.loads(data)
                    if data_json["event"] == "start":
                        stream_sid = data_json.get("streamSid")
                        call_sid = data_json.get("start", {}).get("callSid")
                        print(f"Call started with SID: {call_sid}")
                    elif (
                        data_json["event"] == "media"
                        and "payload" in data_json["media"]
                    ):
                        payload = data_json["media"]["payload"]
                        # Send audio to OpenAI
                        audio_append = {
                            "type": "input_audio_buffer.append",
                            "audio": payload,
                        }
                        await openai_ws.send(json.dumps(audio_append))
            except WebSocketDisconnect:
                print("WebSocket connection closed")

        async def receive_from_openai() -> None:
            nonlocal stream_sid
            nonlocal call_sid
            nonlocal link_sent
            previous_response_type = None
            function_name = None
            try:
                async for openai_message in openai_ws:
                    response = json.loads(openai_message)
                    if response["type"] == "response.audio.delta" and response.get(
                        "delta"
                    ):
                        # Stream audio back to Twilio
                        audio_delta = {
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {"payload": response["delta"]},
                        }
                        await websocket.send_json(audio_delta)

                    elif response["type"] == "response.function_call_arguments.done":
                        function_name = response["name"]

                    elif response["type"] == "response.done":
                        HARVEY_PHONE_NUMBER: str = os.environ.get("HARVEY_PHONE_NUMBER")

                        if function_name == "transfer_call":
                            try:
                                await asyncio.sleep(5)
                                print(
                                    f"Transferring call sid {call_sid} to {HARVEY_PHONE_NUMBER}"
                                )
                                transfer_call(call_sid, HARVEY_PHONE_NUMBER)
                                print(f"Call transferred to {HARVEY_PHONE_NUMBER}")
                            except Exception as e:
                                print(f"Error transferring call: {e}")

                        elif function_name == "schedule_call":
                            phone_number = get_caller_number(call_sid)
                            try:
                                await asyncio.sleep(5)
                                if not link_sent:
                                    schedule_call(phone_number)
                                    print(f"Scheduling link sent to {phone_number}")
                                    link_sent = True
                            except Exception as e:
                                print(f"Error scheduling call: {e}")

                        elif function_name == "hang_up":
                            try:
                                await asyncio.sleep(5)
                                end_call(call_sid)
                            except Exception as e:
                                print(f"Error ending call: {e}")

                        else:
                            if function_name:
                                print(f"Unknown function call: {function_name}")

                    else:
                        if previous_response_type != response["type"]:
                            # print(f"response type: {response['type']}")
                            previous_response_type = response["type"]
                        # print(f"response: {response}")

            except Exception as e:
                print(f"Error in receive_from_openai: {e}")

        await asyncio.gather(receive_from_twilio(), receive_from_openai())


async def send_session_update(openai_ws) -> None:
    """Send session update to OpenAI WebSocket."""
    events = get_events_for_today()
    system_prompt = (
        "You are a personal assistant named Donna, with the personality and mannerisms of Donna from Suits. Donna's personality traits include:"
        "Intelligent and Perceptive: Donna possesses an exceptional ability to read people and situations, often anticipating needs and outcomes before others do. Her insights are invaluable to the firm and its clients."
        "Confident and Assertive: She exudes confidence and isn't afraid to speak her mind, even in challenging situations. Donna stands her ground and advocates for what she believes is right."
        "Witty and Charismatic: Known for her sharp wit and sense of humor, she brings levity to tense situations and is well-liked by her colleagues."
        "Empathetic and Loyal: Donna is deeply caring and goes to great lengths to support those she values, especially Harvey Specter. Her loyalty is unwavering, and she often serves as the emotional backbone for her friends and coworkers."
        "Professional and Resourceful: Highly skilled in her role, Donna is indispensable to the firm's operations. She is organized, efficient, and knows the inner workings of the legal world, even without being a lawyer herself."
        "Your task is to be a personal assistant to Harvey Specter and NOT the firm. You will screen calls by determining the purpose and importance of each call."
        "Categorize the importance as 'none', 'some', or 'very'. Be efficient and direct in your communication, just like Donna would be."
        "You do not need to ask the caller for their phone number, as the tools already have the phone number. Be as concise as possible in your responses."
        "If you suspect the caller is a spammer or scammer, respond with a witty or dismissive comment, then use the hang_up tool to end the call immediately."
        "If the call is not important, politely ask the caller to schedule a call with Harvey by using the schedule_call tool, which will send them a scheduling link."
        "If the call is 'some' importance, then use the following events information to check Harvey's schedule for today and if he's free, transfer the call to Harvey using the transfer_call tool. Otherwise, just ask the caller to schedule a call at the link you're sending them and then use the schedule_call tool, insisting that he's busy right now."
        f"If the caller asks when Harvey is free next, tell them the specific time the current event ends. {events}"
        "If the call is important, transfer the call to Harvey using the transfer_call tool. Only transfer the call if it's very important or from a family member, otherwise just ask the caller to schedule a call at the link you're sending them and then use the schedule_call tool."
        "Always end the call with a brief, natural-sounding sign-off that fits the context of the conversation. Vary your sign-offs to sound more human-like. After the sign-off, use the appropriate tool (hang_up, schedule_call, or transfer_call) to end the interaction."
    )
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": "alloy",
            "instructions": system_prompt,
            "modalities": ["text", "audio"],
            "temperature": 0.7,
            "tools": [
                {
                    "type": "function",
                    "name": "transfer_call",
                    "description": "Transfers an ongoing call to Harvey's phone number.",
                },
                {
                    "type": "function",
                    "name": "schedule_call",
                    "description": "Schedules a call by sending a scheduling link to the provided phone number.",
                },
                {
                    "type": "function",
                    "name": "hang_up",
                    "description": "Ends the current call.",
                },
            ],
            "tool_choice": "auto",
        },
    }
    await openai_ws.send(json.dumps(session_update))
