# Doc: https://docs.python.org/3/library/http.server.html

import os
import json
import structlog
from dotenv import load_dotenv

from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
    SimpleHTTPRequestHandler,
)

from api_complete import (
    get_llm_response,
    get_dummy_llm_response,
)


load_dotenv()
logger = structlog.get_logger(__name__)


class CustomHandler(BaseHTTPRequestHandler):
    """
    Python built in http server handler.
    Handles GET and POST requests for API.
    """

    def do_GET(self):
        if self.path == "/healthz/":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok\n")
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"invalid endpoint\n")

    def do_POST(self):
        if not self.path == "/inference/":
            # If the endpoint is not recognized, return 404
            self.send_response(404)
            self.end_headers()
            response = {"error": "Invalid endpoint"}
            self.wfile.write(json.dumps(response).encode())
            return

        # Handle POST request to /inference/
        try:
            logger.info("[POST] /inference/", client_addr=self.client_address[0])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            status, response = get_llm_response(data)  # inference processor
            self.send_response(status)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=4).encode())
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON in request", exc=exc)
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"error": "Invalid JSON", "full_exc": str(exc)}
            self.wfile.write(json.dumps(response).encode())
            return
        except Exception as exc:
            logger.error("Error processing request", exc=exc)
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"error": "Internal Server Error", "full_exc": str(exc)}
            self.wfile.write(json.dumps(response).encode())
            return


def run(
    host="0.0.0.0",
    port=8000,
    server_class=HTTPServer,
    handler_class=CustomHandler,  # SimpleHTTPRequestHandler
):
    server_address = (host, port)
    logger.info(f"Running Server at {server_address}")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    HOST = os.getenv("HOST", "localhost")
    PORT = int(os.getenv("PORT", 8000))
    run(host="0.0.0.0", port=PORT)
