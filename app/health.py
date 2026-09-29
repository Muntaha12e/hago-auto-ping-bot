import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Dict


class HealthHandler(BaseHTTPRequestHandler):
    """Small standard-library HTTP server for monitoring the bot."""

    stats_provider: Callable[[], Dict[str, Any]]

    def do_GET(self) -> None:  # noqa: N802
        if self.path not in ("/health", "/stats"):
            self.send_error(404, "Not found")
            return

        payload = self.stats_provider()
        payload["status"] = "ok"
        body = json.dumps(payload).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        # Avoid printing every health-check request to stdout.
        return


def start_health_server(stats_provider: Callable[[], Dict[str, Any]], host: str, port: int) -> ThreadingHTTPServer:
    """Start the monitoring endpoint in a daemon thread."""
    handler = type("ConfiguredHealthHandler", (HealthHandler,), {})
    handler.stats_provider = stats_provider

    server = ThreadingHTTPServer((host, port), handler)
    thread = threading.Thread(target=server.serve_forever, name="health-server", daemon=True)
    thread.start()
    return server
