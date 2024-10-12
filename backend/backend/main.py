from fastapi import Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi import FastAPI
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import os

app = FastAPI()


@app.get("/hello")
def hello() -> dict[str, str]:
    return {"Hello": "World"}


STREAM_URL = ""
TWILIO_PHONE_NUMBER = ""


class CallRequest(BaseModel):
    phone_number: str = Field(..., description="The phone number to call")
    call_context: str = Field(..., description="The context of the call")
    agent_id: str = Field(..., description="The ID of the agent")


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
    phone_number = request.phone_number
    call_context = request.call_context
    agent_id = request.agent_id

    print(
        f"phone_number: {phone_number}, call_context: {call_context}, agent_id: {agent_id}"
    )

    if phone_number and agent_id and call_context:
        twiml_response = f"""<Response>
                <Connect>
                    <Stream url="{STREAM_URL}">
                        <Parameter name="agent_id" value="{agent_id}"/>
                        <Parameter name="call_context" value="{call_context}"/>
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
    else:
        return JSONResponse(status_code=400, content={"message": "Invalid request"})
