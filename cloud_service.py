import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from financial_reporter import send_daily_market_update

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def _handle_request(self):
        try:
            logger.info("Cloud Run request received. Running market update check...")
            result = send_daily_market_update()
            payload = json.dumps({"status": "ok" if result else "completed"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except Exception as exc:
            logger.exception("Unhandled error in cloud execution")
            payload = json.dumps({"status": "error", "message": str(exc)}).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    def log_message(self, format, *args):
        logger.info("%s - - [%s] %s", self.address_string(), self.log_date_time_string(), format % args)


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    logger.info(f"Starting cloud service on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
