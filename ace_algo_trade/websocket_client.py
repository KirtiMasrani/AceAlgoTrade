import threading
import time
from typing import Callable, Optional

import websocket


class WebSocketClient:
    """Maintain a resilient WebSocket connection with heartbeat and reconnection."""

    def __init__(
        self,
        url: str,
        on_message: Callable[[str], None],
        *,
        heartbeat_interval: int = 30,
        reconnect_delay: int = 5,
    ) -> None:
        self.url = url
        self.on_message = on_message
        self.heartbeat_interval = heartbeat_interval
        self.reconnect_delay = reconnect_delay
        self.ws: Optional[websocket.WebSocket] = None
        self.stop_event = threading.Event()
        self._hb_thread: Optional[threading.Thread] = None
        self._listen_thread: Optional[threading.Thread] = None

    def connect(self) -> None:
        """Establish the WebSocket connection."""
        self._connect()

    def _connect(self) -> None:
        while not self.stop_event.is_set():
            try:
                self.ws = websocket.create_connection(self.url)
                self._start_threads()
                break
            except Exception:
                time.sleep(self.reconnect_delay)

    def _start_threads(self) -> None:
        self._listen_thread = threading.Thread(target=self._listener, daemon=True)
        self._listen_thread.start()
        self._hb_thread = threading.Thread(target=self._heartbeat, daemon=True)
        self._hb_thread.start()

    def _listener(self) -> None:
        while not self.stop_event.is_set():
            try:
                msg = self.ws.recv()
                if msg is None:
                    raise websocket.WebSocketConnectionClosedException()
                self.on_message(msg)
            except Exception:
                self._reconnect()
                break

    def _heartbeat(self) -> None:
        while not self.stop_event.is_set():
            try:
                self.ws.ping()
            except Exception:
                self._reconnect()
                break
            time.sleep(self.heartbeat_interval)

    def _reconnect(self) -> None:
        if self.stop_event.is_set():
            return
        time.sleep(self.reconnect_delay)
        self._connect()

    def close(self) -> None:
        self.stop_event.set()
        if self.ws:
            try:
                self.ws.close()
            finally:
                self.ws = None
