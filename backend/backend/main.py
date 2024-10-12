from fastapi import Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi import FastAPI
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import os
from fastapi import WebSocket, WebSocketDisconnect


app = FastAPI()


@app.get("/hello")
def hello() -> dict[str, str]:
    return {"Hello": "World"}


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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")

            # Echo the received message back to the client
            await websocket.send_text(f"Echo: {data}")

            # You can add your custom processing logic here
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()