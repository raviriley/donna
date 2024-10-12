
import websockets
import asyncio
import base64
from utils.print_timestamp import print_with_timestamp
import json
from queue import Queue
import uuid
from dotenv import load_dotenv
from aiohttp import web
from datetime import datetime, timedelta
import os
import requests

load_dotenv()

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

        # Add custom input paramters here:

        # try:
        #     self.patient_name = data['start']['customParameters']['patient_name']
        # except KeyError:
        #     self.patient_name = ""

        # today = datetime.today().strftime("%Y-%m-%d")
        # get_day = datetime.today().strftime("%A")

        ## This is the system prompt for the first agent which replies
        ## to the initial user query
        
        #self.assistant = ConversationAgent(cm, cm2, agent_name, self.agent1, self.agent2, tools, tool_map, context_turns=10, intro=intro, audioState=self.AudioState, obj=self)
        
        # call_data = {
        #     'client': client_id,
        #     'from': '',
        #     'to': dart_phone_number,
        #     'call_id': self.sid,
        #     'recording_id': str(self.recording_id),
        # }
        # try:
        #     self.callerId = data['start']['callSid']
        #     self.phone_number = get_caller_number(self.callerId)
        #     call_data['from'] = self.phone_number
        #     print_with_timestamp(f"E-mail: {self.email}")
        #     print_with_timestamp(f"Phone Number: {self.phone_number}")
        # except:
        #     print_with_timestamp("No Caller ID and Phone Number")
        # text = intro
        # self.last_message = datetime.now()
        # self.last_message_id = uuid.uuid4()
        # send_media(ws=self.ws, text=text, sid=self.sid, duration=None, audioState=self.AudioState, obj=self, message_id=self.last_message_id)

    async def handle_stop_event(self):
        # Handle stop event here
        print_with_timestamp("Call Ended")

    async def handle_media_event(self, data):
        # Handle media event here
        media = data["media"]
        payload = base64.b64decode(media["payload"])

        print_with_timestamp(f"Received media event with payload: {payload}")
        
        # Access audio from Twilio
        # Placeholder: Process the audio payload here

    async def run(self):
        print("New Connection Initiated")
        try:
            while not self.ws.closed:
                try:
                    message = await asyncio.wait_for(self.ws.recv(), timeout=20)
                    
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

                except asyncio.TimeoutError:
                    # No data in 20 seconds, check the connection.
                    try:
                        pong_waiter = await self.ws.ping()
                        await asyncio.wait_for(pong_waiter, timeout=10)
                    except asyncio.TimeoutError:
                        # No response to ping in 10 seconds, disconnect.
                        break
                    continue
                except websockets.exceptions.ConnectionClosed:
                    break
                except Exception as e:
                    print_with_timestamp(f"Error: {e}")
                    break
        except Exception as e:
            print_with_timestamp(f"Error: {e}")
        finally:
            await self.ws.close()
            print("WebSocket connection closed")

async def echo(ws, path):
    agent_connection = AgentConnection(ws)
    await agent_connection.run()

async def health(request):
    return web.Response(text="Server is healthy")

async def main():
    while True:
        try:
            server = await websockets.serve(echo, "localhost", 8050)
            print("WebSocket server for the agent started on ws://0.0.0.0:8050")

            app = web.Application()
            app.router.add_get('/health', health)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, '0.0.0.0', 8081)
            await site.start()

            await server.wait_closed()
        except Exception as e:
            print(f"WebSocket server crashed with error: {e}. Restarting...")
            await asyncio.sleep(1)  # Delay before restarting to avoid rapid crash loops

if __name__ == "__main__":
    asyncio.run(main())