__author__ = "Ruu3f"
__version__ = "1.0.1"

from time import sleep
from uuid import uuid4
from requests import Session
from threading import Thread
from json import loads, dumps
from random import getrandbits
from websocket import WebSocketApp


class Completion:
    def __init__(self):
        self.is_websocket_connecting = False
        self.is_websocket_connected = False
        self.session = Session()
        self.is_searching = False
        self.request_number = 0

    async def create(self, prompt):
        def on_message(ws, message):
            try:
                if message == "2":
                    ws.send("3")
                elif message == "3probe":
                    ws.send("5")

                if (
                    self.is_searching or self.asking_for_details
                ) and message.startswith(str(430 + self.request_number)):
                    response = loads(message[3:])[0]

                    if self.is_searching:
                        self.answer = {
                            "uuid": response["uuid"],
                            "gpt4": response["gpt4"],
                            "text": response["text"],
                            "search_focus": response["search_focus"],
                            "backend_uuid": response["backend_uuid"],
                            "query_str": response["query_str"],
                            "related_queries": response["related_queries"],
                        }
                        self.is_searching = False
                    else:
                        self.answer["details"] = {
                            "uuid": response["uuid"],
                            "text": response["text"],
                        }
                        self.asking_for_details = False
            except:
                raise Exception("Unable to fetch the response.")
                self.is_websocket_connecting = False
                self.is_websocket_connected = False
                if self.websocket:
                    self.websocket.close()
                self.connect_websocket()

        def init_websocket(timeout=5):
            if self.is_websocket_connected:
                return
            if self.is_websocket_connecting:
                while not self.is_websocket_connected:
                    sleep(0.01)
                return
            self.is_websocket_connecting = True
            self.is_websocket_connected = False

            ws_url = f"wss://www.perplexity.ai/socket.io/?EIO=4&transport=websocket&sid={self.sid}"

            cookie = ""
            for key, value in self.session.cookies.get_dict().items():
                cookie += f"{key}={value}; "

            self.websocket = WebSocketApp(
                url=ws_url,
                header={"User-Agent": ""},
                cookie=cookie,
                on_open=lambda ws: on_websocket_connect(ws),
                on_message=on_message,
                on_error=lambda ws, error: on_websocket_error(error),
                on_close=lambda ws: on_websocket_close(ws),
            )
            websocket_thread = Thread(target=self.websocket.run_forever)
            websocket_thread.daemon = True
            websocket_thread.start()

            timer = 0
            while not self.is_websocket_connected:
                sleep(0.01)
                timer += 0.01
                if timer > timeout:
                    self.is_websocket_connecting = False
                    self.is_websocket_connected = False
                    self.websocket.close()
                    raise RuntimeError(
                        "Timed out waiting for the websocket to connect."
                    )

        def on_websocket_connect(ws):
            self.is_websocket_connecting = False
            self.is_websocket_connected = True
            ws.send("2probe")

        def on_websocket_error():
            raise Exception("Unable to fetch the response.")
            self.is_websocket_connecting = False
            self.is_websocket_connected = False
            if self.websocket:
                self.websocket.close()
            self.connect_websocket()

        def on_websocket_close(ws):
            self.is_websocket_connecting = False
            self.is_websocket_connected = False
            self.connect_websocket()

        assert not self.is_searching, "Already searching"
        assert "internet" in [
            "internet",
            "scholar",
            "news",
            "youtube",
            "reddit",
            "wikipedia",
        ]
        self.is_searching = True
        self.request_number += 1
        self.session.get(
            url=f"https://www.perplexity.ai/search/{str(uuid4())}",
            headers={"User-Agent": ""},
        )
        self.t = format(getrandbits(32), "08x")
        self.sid = loads(
            self.session.get(
                url=f"https://www.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}",
                headers={"User-Agent": ""},
            ).text[1:]
        )["sid"]
        self.frontend_uuid = str(uuid4())
        self.frontend_session_id = str(uuid4())

        assert self.session.post(
            url=f"https://www.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}&sid={self.sid}",
            data='40{"jwt":"anonymous-ask-user"}',
            headers={"User-Agent": ""},
        ).text, "Failed to ask anonymous user"
        self.websocket = None
        init_websocket()

        self.session.get(
            url="https://www.perplexity.ai/api/auth/session", headers={"User-Agent": ""}
        )

        sleep(1)

        ws_message = f"{420 + self.request_number}" + dumps(
            [
                "perplexity_ask",
                prompt,
                {
                    "source": "default",
                    "last_backend_uuid": None,
                    "read_write_token": "",
                    "conversational_enabled": True,
                    "frontend_session_id": self.frontend_session_id,
                    "search_focus": "internet",
                    "frontend_uuid": self.frontend_uuid,
                    "web_search_images": True,
                    "gpt4": False,
                },
            ]
        )
        self.websocket.send(ws_message)
        while self.is_searching:
            sleep(0.1)

        return loads(self.answer["text"])["answer"]
