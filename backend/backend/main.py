from fastapi import Depends
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


app = FastAPI()


class CallRequest(BaseModel):
    phone_number: str = Field(..., description="The phone number to call")
    # call_context: str = Field(..., description="The context of the call")
    # agent_id: str = Field(..., description="The ID of the agent")


def get_twilio_client() -> TwilioClient:
    load_dotenv()
    account_sid: str = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token: str = os.environ.get("TWILIO_AUTH_TOKEN")
    return TwilioClient(account_sid, auth_token)


@app.post("/calls/outbound")
async def trigger_outbound_call(
    request: CallRequest,
    twilio_client: TwilioClient = Depends(get_twilio_client),
) -> JSONResponse:
    print(request)

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


def transfer_call(call_sid: str, new_phone_number: str) -> None:
    """Transfers an existing call to a different phone number mid-stream."""
    twiml_response = f"""<Response>
                <Dial>{new_phone_number}</Dial>
            </Response>"""
    twilio_client = get_twilio_client()
    twilio_client.calls(call_sid).update(twiml=twiml_response)
    print(f"Call transferred to {new_phone_number} with Call SID: {call_sid}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    call_sid = None  # Initialize call_sid to store the call ID

    # Load environment variables
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

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

        async def receive_from_twilio():
            nonlocal call_sid
            try:
                while True:
                    data = await websocket.receive_text()
                    data_json = json.loads(data)
                    if data_json["event"] == "start":
                        call_sid = data_json.get("streamSid")
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

        async def receive_from_openai():
            try:
                async for openai_message in openai_ws:
                    response = json.loads(openai_message)
                    if response["type"] == "response.audio.delta" and response.get(
                        "delta"
                    ):
                        # Stream audio back to Twilio
                        audio_delta = {
                            "event": "media",
                            "streamSid": call_sid,
                            "media": {"payload": response["delta"]},
                        }
                        await websocket.send_json(audio_delta)
            except Exception as e:
                print(f"Error in receive_from_openai: {e}")

        await asyncio.gather(receive_from_twilio(), receive_from_openai())


async def send_session_update(openai_ws):
    """Send session update to OpenAI WebSocket."""
    system_prompt = (
        "You are a personal assistant named Donna, with the personality and mannerisms of Donna from Suits. "
        "Your task is to screen calls by determining the purpose and importance of each call. "
        "Categorize the importance as 'none', 'some', or 'very'. Be efficient and direct in your communication, "
        "just like Donna would be."
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
        },
    }
    print("Sending session update:", json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))
