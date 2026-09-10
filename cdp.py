import json
import urllib.request
import websocket

class ChromiumDevTools:

    def __init__(self, port=9222):
        self.url = f"http://127.0.0.1:{port}/json/list"
        self.ws = None
        self.message_id = 1

    # --------------------------------------------------
    # Find YouTube tab
    # --------------------------------------------------

    def _find_youtube_tab(self):
        with urllib.request.urlopen(self.url) as response:
            targets = json.load(response)

        for target in targets:
            if (
                target["type"] == "page"
                and "youtube.com" in target["url"]
            ):
                return target

        raise RuntimeError("YouTube tab not found.")

    # --------------------------------------------------
    # Connect to YouTube tab
    # --------------------------------------------------

    def connect(self):
        target = self._find_youtube_tab()

        self.ws = websocket.create_connection(
            target["webSocketDebuggerUrl"]
        )

        return target

    # --------------------------------------------------
    # Send CDP command
    # --------------------------------------------------

    def _send(self, method, params=None):
        if self.ws is None:
            raise RuntimeError("BravePlayer is not connected.")

        self.message_id += 1

        message = {
            "id": self.message_id,
            "method": method,
        }

        if params:
            message["params"] = params

        self.ws.send(json.dumps(message))

        return json.loads(self.ws.recv())

    # --------------------------------------------------
    # Execute JavaScript
    # --------------------------------------------------

    def _evaluate(self, expression):
        response = self._send(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
            }
        )

        result = response.get("result", {})
        return result.get("result", {}).get("value")

    # --------------------------------------------------
    # Load YouTube video
    # --------------------------------------------------

    def load(self, url):
        self._send(
            "Page.navigate",
            {
                "url": url
            }
        )

    # --------------------------------------------------
    # Play
    # --------------------------------------------------

    def play(self):
        return self._evaluate(
            """
            (() => {
                const video = document.querySelector('video');

                if (!video) {
                    return 'Video element not found';
                }

                video.play();

                return 'Playing';
            })()
            """
        )

    # --------------------------------------------------
    # Pause
    # --------------------------------------------------

    def pause(self):
        return self._evaluate(
            """
            (() => {
                const video = document.querySelector('video');

                if (!video) {
                    return 'Video element not found';
                }

                video.pause();

                return 'Paused';
            })()
            """
        )

    # --------------------------------------------------
    # Check if is playing
    # --------------------------------------------------

    def is_playing(self):
        return self._evaluate(
            """
            (() => {
                const video = document.querySelector('video');

                if (!video) {
                    return false;
                }

                return !video.paused && !video.ended;
            })()
            """
        )

    # --------------------------------------------------
    # Check if ended
    # --------------------------------------------------
    def is_ended(self):
        return self._evaluate(
            """
            (() => {
                const video = document.querySelector('video');

                if (!video) {
                    return false;
                }

                return video.ended;
            })()
            """
        )

    # --------------------------------------------------
    # Close connection
    # --------------------------------------------------

    def disconnect(self):
        if self.ws:
            self.ws.close()
            self.ws = None