import websocket
import time
import signal
import ssl

class defaultWebsocketApp():
    addr = "ws://bbean.us:8080"
    websocketList = [None]
    on_message_handler = None

    def __init__(self, on_message_handler=None):
        self.on_message_handler = on_message_handler

    def signal_handler(self, signal, frame):
        self.close()

    def on_message(self, ws, message):
        if (self.on_message_handler is None):
            print(message)
        else:
            self.on_message_handler(ws, message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        self.websocketList[0] = None
        print("### closed ###")

    def on_open(self, ws):
        print("connected")

    def close(self):
        if (self.websocketList[0] is None):
            print("there is no websocket to close")
        else:
            print("closing")
            ws.close()

    def start(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.addr,
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        self.websocketList[0] = ws
        ws.on_open = self.on_open
        print("connecting to websocket at \"" + self.addr + "\"")
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})