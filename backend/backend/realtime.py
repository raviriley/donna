import websocket
import json
import threading


class OpenAIRealtimeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.ws = None
        self.thread = None
        self.events = []
        self.connect()

    def connect(self):
        """
        Establish a WebSocket connection to the OpenAI Realtime API.
        """
        self.ws = websocket.WebSocketApp(
            "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview",
            header={
                "Authorization": f"Bearer {self.api_key}",
                "openai-beta": "realtime=v1",
            },
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open,
        )
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()

    def close(self):
        """
        Close the WebSocket connection and join the thread.
        """
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()

    def _on_message(self, ws, message):
        """
        Handle incoming WebSocket messages.
        """
        data = json.loads(message)
        self.events.append(data)  # Store the received event in the events list

    def _on_error(self, ws, error):
        """
        Handle WebSocket errors.
        """
        print(f"Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        """
        Handle WebSocket closure.
        """
        print(f"WebSocket connection closed: {close_status_code} - {close_msg}")

    def _on_open(self, ws):
        """
        Handle WebSocket connection opening.
        """
        print("WebSocket connection opened")

    def send_raw_event(self, event):
        """
        Send a raw event to the WebSocket.

        :param event: A dictionary representing the event to send.
        """
        if self.ws and self.ws.sock and self.ws.sock.connected:
            self.ws.send(json.dumps(event))
        else:
            print("WebSocket is not connected")

    # Methods for sending specific types of events
    def send_session_update(self, session_config):
        event = {"type": "session.update", "session": session_config}
        self.send_raw_event(event)

    def append_audio(self, audio_bytes_base64):
        event = {
            "type": "input_audio_buffer.append",
            "audio": audio_bytes_base64,
        }
        self.send_raw_event(event)

    def commit_audio(self):
        event = {"type": "input_audio_buffer.commit"}
        self.send_raw_event(event)

    def clear_audio_buffer(self):
        event = {"type": "input_audio_buffer.clear"}
        self.send_raw_event(event)

    def create_conversation_item(self, item, previous_item_id=None):
        event = {
            "type": "conversation.item.create",
            "previous_item_id": previous_item_id,
            "item": item,
        }
        self.send_raw_event(event)

    def truncate_conversation_item(self, item_id, content_index, audio_end_ms):
        event = {
            "type": "conversation.item.truncate",
            "item_id": item_id,
            "content_index": content_index,
            "audio_end_ms": audio_end_ms,
        }
        self.send_raw_event(event)

    def delete_conversation_item(self, item_id):
        event = {"type": "conversation.item.delete", "item_id": item_id}
        self.send_raw_event(event)

    def create_response(self, response_config):
        event = {"type": "response.create", "response": response_config}
        self.send_raw_event(event)

    def cancel_response(self):
        event = {"type": "response.cancel"}
        self.send_raw_event(event)

    def __del__(self):
        """
        Ensure the WebSocket connection is properly closed when the instance is deleted.
        """
        self.close()
