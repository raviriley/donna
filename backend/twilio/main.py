from flask import Flask, jsonify
import base64
from utils.print_timestamp import print_with_timestamp
import json
import os
import requests
from dotenv import load_dotenv
from flask_sockets import Sockets

load_dotenv()

app = Flask(__name__)
sockets = Sockets(app)

dart_phone_number = '+13234725518'

def get_caller_number(call_sid):
    # Twilio API base URL
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    base_url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Calls/{call_sid}.json'
    auth_header = (account_sid, auth_token)
    response = requests.get(base_url, auth=auth_header)
    if response.status_code == 200:
        to = response.json()['to']
        from_number = response.json()['from']
        # check if the number is the dart number
        if to == dart_phone_number:
            return from_number
        else:
            return to
    else:
        return ''

class AgentConnection:
    def __init__(self, ws):
        self.ws = ws
        self.sid = None
        self.callerId = None
        self.phone_number = ''

    async def handle_start_event(self, data):
        # Handle start event here
        print_with_timestamp("Websocket Connected")

        print(data)

    async def handle_stop_event(self):
        # Handle stop event here
        print_with_timestamp("Call Ended")

    async def handle_media_event(self, data):
        # Handle media event here
        media = data["media"]
        payload = base64.b64decode(media["payload"])

        print_with_timestamp(f"Received media event with payload: {payload}")

    async def run(self):
        print("New Connection Initiated")
        try:
            while not self.ws.closed:
                try:
                    message = await self.ws.receive()
                    
                    if message is None:
                        continue

                    data = json.loads(message)
                    if self.sid is None:
                        self.sid = data.get("streamSid")

                    if data.get("event") == "start":
                        await self.handle_start_event(data)

                    if data.get("event") == "stop":
                        await self.handle_stop_event()

                    if data.get("event") == "media":
                        await self.handle_media_event(data)

                except Exception as e:
                    print_with_timestamp(f"Error: {e}")
                    break
        except Exception as e:
            print_with_timestamp(f"Error: {e}")
        finally:
            self.ws.close()
            print("WebSocket connection closed")

@sockets.route('/echo')
def echo(ws):
    agent_connection = AgentConnection(ws)
    asyncio.run(agent_connection.run())

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"message": "Server is healthy"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)