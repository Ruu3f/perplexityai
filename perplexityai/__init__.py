__author__ = "Ruu3f"
__version__ = "1.0.5"

from uuid import uuid4
from requests import Session
from time import sleep, time
from threading import Thread
from json import loads, dumps
from random import getrandbits
from websocket import WebSocketApp


class Perplexity:
    def __init__(self):
        self.session = Session()
        self.user_agent = {
            "User-Agent": "Ask/2.4.1/224 (iOS; iPhone; Version 17.1) isiOSOnMac/false",
            "X-Client-Name": "Perplexity-iOS",
        }
        self.session.headers.update(self.user_agent)
        self.t = format(getrandbits(32), "08x")
        response = self.session.get(
            url=f"https://www.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}"
        ).text[1:]
        self.sid = loads(response)["sid"]
        self.n = 1
        self.base = 420
        self.finished = True
        self.last_uuid = None
        assert (
            lambda: self.session.post(
                url=f"https://www.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}&sid={self.sid}",
                data='40{"jwt":"anonymous-ask-user"}',
            ).text
            == "OK"
        )(), "Failed to ask the anonymous user."
        self.ws = self._init_websocket()
        self.ws_thread = Thread(target=self.ws.run_forever).start()
        while not (self.ws.sock and self.ws.sock.connected):
            sleep(0.1)

    def _init_websocket(self):
        def on_open(ws):
            ws.send("2probe")
            ws.send("5")

        def on_message(ws, message):
            if message == "2":
                ws.send("3")
            elif not self.finished:
                if message.startswith("42"):
                    message = loads(message[2:])
                    content = message[1]
                    if "mode" in content:
                        content.update(loads(content["text"]))
                    content.pop("text")
                    if (not ("final" in content and content["final"])) or (
                        "status" in content and content["status"] == "completed"
                    ):
                        self.queue.append(content)
                    if message[0] == "query_answered":
                        self.last_uuid = content["uuid"]
                        self.finished = True
                elif message.startswith("43"):
                    message = loads(message[3:])[0]
                    if (
                        "uuid" in message and message["uuid"] != self.last_uuid
                    ) or "uuid" not in message:
                        self.queue.append(message)
                        self.finished = True

        cookies = "; ".join(
            [f"{key}={value}" for key, value in self.session.cookies.get_dict().items()]
        )
        ws = WebSocketApp(
            url=f"wss://www.perplexity.ai/socket.io/?EIO=4&transport=websocket&sid={self.sid}",
            header=self.user_agent,
            cookie=cookies,
            on_open=on_open,
            on_message=on_message,
            on_error=lambda ws, err: print(f"WebSocket error: {err}"),
        )
        return ws

    def generate_answer(self, query):
        self.finished = False
        if self.n == 9:
            self.n = 0
            self.base *= 10
        else:
            self.n += 1
        self.queue = []
        self.ws.send(
            str(self.base + self.n)
            + dumps(
                [
                    "perplexity_ask",
                    query,
                    {
                        "frontend_session_id": str(uuid4()),
                        "language": "en-GB",
                        "timezone": "UTC",
                        "search_focus": "internet",
                        "frontend_uuid": str(uuid4()),
                        "mode": "concise",
                    },
                ]
            )
        )
        start_time = time()
        while (not self.finished) or len(self.queue) != 0:
            if time() - start_time > 30:
                self.finished = True
                return {"error": "Timed out."}
            if len(self.queue) != 0:
                yield self.queue.pop(0)
        self.ws.close()


class Labs:
    def __init__(self):
        self.history = []
        self.session = Session()
        self.session.headers.update(
            {
                "User-Agent": "Ask/2.2.1/334 (iOS; iPhone) isiOSOnMac/false",
                "X-Client-Name": "Perplexity-iOS",
            }
        )
        self.session.get(url=f"https://www.perplexity.ai/search/{str(uuid4())}")
        self.t = format(getrandbits(32), "08x")
        response = self.session.get(
            url="https://labs-api.perplexity.ai/socket.io/?transport=polling&EIO=4"
        ).text[1:]
        self.sid = loads(response)["sid"]

        self.queue = []
        self.finished = True

        response = self.session.post(
            url=f"https://labs-api.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}&sid={self.sid}",
            data='40{"jwt":"anonymous-ask-user"}',
        ).text
        assert response == "OK", "failed to ask anonymous user"

        self._init_websocket()

        while not (self.ws.sock and self.ws.sock.connected):
            sleep(0.01)

    def _init_websocket(self):
        def on_open(ws):
            ws.send("2probe")
            ws.send("5")

        def on_message(ws, message):
            if message == "2":
                ws.send("3")
            elif message.startswith("42"):
                message = loads(message[2:])[1]
                if "status" not in message:
                    self.queue.append(message)
                elif message["status"] == "completed":
                    self.finished = True
                    self.history.append(
                        {
                            "role": "assistant",
                            "content": message["output"],
                            "priority": 0,
                        }
                    )
                elif message["status"] == "failed":
                    self.finished = True

        cookies = "; ".join(
            [f"{key}={value}" for key, value in self.session.cookies.get_dict().items()]
        )
        self.ws = WebSocketApp(
            url=f"wss://labs-api.perplexity.ai/socket.io/?EIO=4&transport=websocket&sid={self.sid}",
            header={
                "User-Agent": "Ask/2.2.1/334 (iOS; iPhone) isiOSOnMac/false",
                "Cookie": cookies,
            },
            on_open=on_open,
            on_message=on_message,
            on_error=lambda ws, err: print(f"websocket error: {err}"),
        )
        Thread(target=self.ws.run_forever).start()
        self.session.get(url="https://www.perplexity.ai/api/auth/session")

    def generate_answer(self, prompt, model="mistral-7b-instruct"):
        assert self.finished, "already searching"
        assert model in [
            "mixtral-8x7b-instruct",
            "llava-7b-chat",
            "llama-2-70b-chat",
            "codellama-34b-instruct",
            "mistral-7b-instruct",
            "pplx-7b-chat",
            "pplx-70b-chat",
            "pplx-7b-online",
            "pplx-70b-online",
        ]
        self.finished = False
        self.history.append({"role": "user", "content": prompt, "priority": 0})
        self.ws.send(
            f'42["perplexity_labs",{{"version":"2.2","source":"default","model":"{model}","messages":{dumps(self.history)}}}]'
        )

        while (not self.finished) or (len(self.queue) != 0):
            if len(self.queue) > 0:
                yield self.queue.pop(0)
        self.ws.close()
