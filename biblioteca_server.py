from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit
import json


BOOKS = [
    {
        "id": 1,
        "title": "Dom Casmurro",
        "author": "Machado de Assis",
        "description": "Dom Casmurro é um romance realista publicado em 1899 pelo escritor brasileiro Machado de Assis.",
        "year": 1899,
        "available": True,
    },
    {
        "id": 2,
        "title": "O Cortico",
        "author": "Aluisio Azevedo",
        "description": "O Cortiço é um romance publicado em 1890 pelo escritor brasileiro Aluísio Azevedo, considerado a obra máxima do Naturalismo no Brasil.",
        "year": 1890,
        "available": True,
    },
]


class BibliotecaHTTPRequestHandler(BaseHTTPRequestHandler):

    def _send_json(self, status, data=None, headers=None):
        body = b""

        if data is not None:
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8"
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

    def _get_book_id(self):
        book_id_text = self._get_path().split("/")[-1]

        try:
            return int(book_id_text)
        except ValueError:
            self._send_json(400, {"error": "Invalid book ID"})
            return None

    def _find_book(self, book_id):
        return next((book for book in BOOKS if book["id"] == book_id), None)

    def _read_json(self):
        content_length = self.headers.get("Content-Length")

        if content_length is None:
            self._send_json(411, {"error": "Content-Length required"})
            return None

        try:
            length = int(content_length)

            if length < 0:
                raise ValueError

            data = self.rfile.read(length)
            return json.loads(data)

        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "Invalid JSON"})
            return None

    def _validate_book_data(self, book_data):
        if not isinstance(book_data, dict):
            self._send_json(400, {"error": "JSON object expected"})
            return False

        required_fields = ["title", "author", "description", "year", "available"]

        for field in required_fields:
            if field not in book_data:
                self._send_json(400, {"error": f"Field '{field}' is required"}
                )
                return False

        if not isinstance(book_data["title"], str):
            self._send_json(400, {"error": "Field 'title' must be a string"})
            return False

        if not isinstance(book_data["author"], str):
            self._send_json(400, {"error": "Field 'author' must be a string"})
            return False

        if not isinstance(book_data["description"], str):
            self._send_json(400, {"error": "Field 'description' must be a string"})
            return False

        if (not isinstance(book_data["year"], int) or isinstance(book_data["year"], bool)
        ):
            self._send_json(400, {"error": "Field 'year' must be an integer"})
            return False

        if not isinstance(book_data["available"], bool):
            self._send_json(400, {"error": "Field 'available' must be a boolean"})
            return False


        return True

    def do_GET(self):
        path = self._get_path()


        if path == "/api/books":
            self._send_json(200, BOOKS)
            return

        if path == "/api/books/available":
            books_available = [
                book for book in BOOKS if book["available"]
            ]
            self._send_json(200, books_available)
            return

        if path == "/api/books/unavailable":
            books_unavailable = [
                book for book in BOOKS if not book["available"]
            ]
            self._send_json(200, books_unavailable)
            return

        if path.startswith("/api/books/"):
            book_id = self._get_book_id()

            if book_id is None:
                return

            book = self._find_book(book_id)

            if book is None:
                self._send_json(404, {"error": "Book not found"})
                return

            self._send_json(200, book)
            return

        self._send_json(404, {"error": "Route not found"})

    def do_POST(self):
        path = self._get_path()

        if path != "/api/books":
            self._send_json(404, {"error": "Route not found"})
            return

        new_book = self._read_json()

        if new_book is None:
            return

        if not self._validate_book_data(new_book):
            return

        next_id = max((book["id"] for book in BOOKS), default=0) + 1

        new_book["id"] = next_id
        BOOKS.append(new_book)

        self._send_json(201, new_book, headers={"Location": f"/api/books/{next_id}"})

    def do_PUT(self):
        path = self._get_path()

        if not path.startswith("/api/books/"):
            self._send_json(404, {"error": "Route not found"})
            return

        book_id = self._get_book_id()

        if book_id is None:
            return

        book = self._find_book(book_id)

        if book is None:
            self._send_json(404, {"error": "Book not found"})
            return

        updated_book = self._read_json()

        if updated_book is None:
            return

        if not self._validate_book_data(updated_book):
            return

        book["title"] = updated_book["title"]
        book["author"] = updated_book["author"]
        book["description"] = updated_book["description"]
        book["year"] = updated_book["year"]
        book["available"] = updated_book["available"]

        self._send_json(200, book)

    def do_DELETE(self):
        path = self._get_path()

        if not path.startswith("/api/books/"):
            self._send_json(404, {"error": "Route not found"})
            return

        book_id = self._get_book_id()

        if book_id is None:
            return

        for index, book in enumerate(BOOKS):
            if book["id"] == book_id:
                BOOKS.pop(index)
                self._send_json(204)
                return

        self._send_json(404, {"error": "Book not found"})


def run(server_class=HTTPServer,
        handler_class=BibliotecaHTTPRequestHandler,
        port=3001):

    server_address = ("127.0.0.1", port)

    httpd = server_class(server_address, handler_class)

    print(f"Servidor HTTP disponível em "
          f"http://127.0.0.1:{port}")

    httpd.serve_forever()


if __name__ == "__main__":
    run()
