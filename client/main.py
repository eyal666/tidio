from datetime import datetime
import time
import uuid

import websocket
import threading
import json
import sys

visitor_id = str(uuid.uuid4().hex)
# ruyp05soezrqaaboosg6jtkz41zas8bf
public_key = None


def visitor_register_message():
    return "420" + json.dumps([
        "visitorRegister",
        {
            "id": visitor_id,
            "originalVisitorId": visitor_id,
            "distinct_id": None,
            "country": None,
            "name": "",
            "city": None,
            "browser_session_id": "",
            "created": int(time.time()),
            "email": "",
            "project_public_key": public_key,
            "phone": "",
            "ip": None,
            "lang": "en-us",
            "browser": "Chrome",
            "browser_version": 126,
            "url": "http://localhost:8000/",
            "refer": "",
            "os_name": "OS X",
            "os_version": "",
            "screen_width": 2560,
            "screen_height": 1440,
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            "timezone": "Asia/Jerusalem",
            "mobile": False,
            "is_chat_on_site": False,
            "wd": "t",
            "sandbox": False,
            "isDesignMode": False,
            "isProjectOnline": True,
            "cache_hash": str(uuid.uuid4().hex),
            "after_reconnect": False
        }
    ])


def format_visitor_message(message: str) -> str:
    return "427" + json.dumps([
        "visitorNewMessage",
        {
            "message": message,
            "messageId": str(uuid.uuid4()),
            "url": "http://localhost:8000/",
            "visitorId": visitor_id,
            "projectPublicKey": public_key,
            "device": "desktop"
        }
    ])


def on_open(_client: websocket.WebSocket):
    print("Connection established.")


def on_message(_client: websocket.WebSocket, message: str):
    if message.startswith("0{"):
        print("Connection established")
        _client.send("40")
        return

    if message.startswith("40{"):
        print("Tidio ack")
        _client.send(visitor_register_message())
        return

    if message == '42["connected"]':
        print("Tidio connected")
        return

    if message == "2":
        _client.send("3")
        return

    if message.startswith('42["newMessage'):
        parsed_message = json.loads(message[2:])
        parsed_message = parsed_message[1]["data"]["message"]["message"]

        print("Received message: " + parsed_message)
        if parsed_message == "Hi there 👋 If you need any assistance, I'm always here.":
            def send_messages():
                while True:
                    try:
                        _message = input("Enter message: ")
                        _client.send(format_visitor_message(_message))
                    except Exception as e:
                        print(f"Send error: {e}")
                        _client.close()
                        break

            threading.Thread(target=send_messages).start()


def on_error(ws, error):
    print(f"Error: {error}")
    ws.close()
    sys.exit(1)


def on_close(ws, _, __):
    print("Connection closed.")


def init_connection():
    tidio_url = f"wss://socket.tidio.co/socket.io/?ppk={public_key}&device=desktop&cmv=2_0&EIO=4&transport=websocket"
    _client = websocket.WebSocketApp(
        url=tidio_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    return _client


if __name__ == '__main__':
    print("CLI initializing...")
    public_key = input("Provide public key: ")
    if not public_key:
        raise ValueError("Public key is required")

    # todo: add error handling

    client = init_connection()
    client.run_forever()
