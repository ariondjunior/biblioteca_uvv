from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit
import json

USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]


class RestHTTPRequestHandler(BaseHTTPRequestHandler):

    def _send_json(self, status, data=None, headers=None):
        body = b""

        if data is not None:
            body = json.dumps(data).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        if headers:
            for name, value in headers.items():
                self.send_header(name, value)

        if status != 204:
            self.send_header("Content-Length", str(len(body)))

        self.end_headers()

        if body:
            self.wfile.write(body)

    def _get_path(self):
        return urlsplit(self.path).path

    def do_GET(self):
        path = self._get_path()

        if path == "/api/users":
            self._send_json(200, USERS)
            return

        if path.startswith("/api/users/"):
            user_id_text = path.split("/")[-1]

            try:
                user_id = int(user_id_text)
            except ValueError:
                self._send_json(
                    400,
                    {"error": "Invalid user ID"}
                )
                return

            user = next(
                (user for user in USERS if user["id"] == user_id),
                None
            )

            if user is None:
                self._send_json(
                    404,
                    {"error": "User not found"}
                )
                return

            self._send_json(200, user)
            return

        self._send_json(
            404,
            {"error": "Route not found"}
        )

    def do_POST(self):
        path = self._get_path()

        if path != "/api/users":
            self._send_json(
                404,
                {"error": "Route not found"}
            )
            return

        content_length = self.headers.get("Content-Length")

        if content_length is None:
            self._send_json(
                411,
                {"error": "Content-Length required"}
            )
            return

        try:
            length = int(content_length)
            data = self.rfile.read(length)
            new_user = json.loads(data)
        except (ValueError, json.JSONDecodeError):
            self._send_json(
                400,
                {"error": "Invalid JSON"}
            )
            return

        if not isinstance(new_user, dict):
            self._send_json(
                400,
                {"error": "JSON object expected"}
            )
            return

        if "name" not in new_user:
            self._send_json(
                400,
                {"error": "Field 'name' is required"}
            )
            return

        next_id = max(
            (user["id"] for user in USERS),
            default=0
        ) + 1

        new_user["id"] = next_id
        USERS.append(new_user)

        self._send_json(
            201,
            new_user,
            headers={
                "Location": f"/api/users/{next_id}"
            }
        )

    def do_DELETE(self):
        path = self._get_path()

        if not path.startswith("/api/users/"):
            self._send_json(
                404,
                {"error": "Route not found"}
            )
            return

        user_id_text = path.split("/")[-1]

        try:
            user_id = int(user_id_text)
        except ValueError:
            self._send_json(
                400,
                {"error": "Invalid user ID"}
            )
            return

        for index, user in enumerate(USERS):
            if user["id"] == user_id:
                USERS.pop(index)

                self._send_json(204)
                return

        self._send_json(
            404,
            {"error": "User not found"}
        )


def run(
    server_class=HTTPServer,
    handler_class=RestHTTPRequestHandler,
    port=3001
):
    server_address = ("127.0.0.1", port)

    httpd = server_class(
        server_address,
        handler_class
    )

    print(
        f"Servidor HTTP disponível em "
        f"http://127.0.0.1:{port}"
    )

    httpd.serve_forever()


if __name__ == "__main__":
    run()