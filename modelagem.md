# Modelagem da API de Catálogo de Livros

## Representação

Abaixo é mostrado a representação da API, onde cada livo possui os campos `id`, `title`, `author`, `description`, `year`, `available`. Segue o exemplo:

```json
{
  "id": 1,
  "title": "Dom Casmurro",
  "author": "Machado de Assis",
  "description": "Dom Casmurro é um romance realista publicado em 1899 pelo escritor brasileiro Machado de Assis.",
  "year": 1899,
  "available": true
}
```

## Recursos e URIs

| Recurso | URI | Significado |
| --- | --- | --- |
| Coleção de livros | `/api/books` | Representa todos os livros do catálogo. |
| Livro individual | `/api/books/{id}` | Representa um livro identificado pelo seu `id`. |
| Coleção de livros disponíveis | `/api/books/available` | Representa todos os livros disponíveis. |
| Coleção de livros indisponíveis | `/api/books/unavailable` | Representa todos os livros indisponíveis. |

É muito importante saber distinguir que `/api/books` e `/api/books/1` representam recursos diferentes, onde o primeiro é a coleção, enquanto o segundo é um único elemento dessa coleção. Dito isso, abaixo será listado o resgistro de todas as informações relevantes da API.

## Operações

| Método | URI | Código de status |
| --- | --- | --- |
| `GET` | `/api/books` | `200 OK` e a coleção em JSON. |
| `GET` | `/api/books/{id}` | `200 OK` e o livro em JSON. |
| `GET` | `/api/books/available` | `200 OK` e os livros disponíveis em JSON. |
| `GET` | `/api/books/unavailable` | `200 OK` e os livros indisponíveis em JSON. |
| `POST` | `/api/books` | `201 Created`, o livro criado e o cabeçalho `Location`. |
| `PUT` | `/api/books/{id}` | `200 OK` e o livro atualizado em JSON. |
| `DELETE` | `/api/books/{id}` | `204 No Content`, sem corpo de resposta. |


## Erros tratados

| Situação | Status | Resposta |
| --- | --- | --- |
| Identificador inválido | `400 Bad Request` | `{"error": "Invalid book ID"}` |
| JSON com formatação inválida | `400 Bad Request` | `{"error": "Invalid JSON"}` |
| Corpo JSON que não é objeto | `400 Bad Request` | `{"error": "JSON object expected"}` |
| Campo obrigatório ausente | `400 Bad Request` | `Mensagem informando o campo.` |
| Tipo de campo incompatível | `400 Bad Request` | `Mensagem informando o campo.` |
| Livro inexistente | `404 Not Found` | `{"error": "Book not found"}` |
| Rota não definida | `404 Not Found` | `{"error": "Route not found"}` |
| Corpo sem `Content-Length` | `411 Length Required` | `{"error": "Content-Length required"}` |

## Comandos curl para demonstração

Para iniciar o servidor e testar a API é necessário rodar esse comando abaixo no terminal:

```bash
python3 biblioteca_server.py
```

Em outro terminal, execute os comandos abaixo na ordem apresentada. Para mostrar o cabeçalho execute com a flag `-i`

### GET

Listar todos os livros:

```bash
curl -i -X GET \
  http://127.0.0.1:3001/api/books
```

Consultar o livro de identificador `1`:

```bash
curl -i -X GET \
  http://127.0.0.1:3001/api/books/1
```

Listar somente os livros disponíveis:

```bash
curl -i -X GET \
  http://127.0.0.1:3001/api/books/available
```

Listar somente os livros indisponíveis:

```bash
curl -i -X GET \
  http://127.0.0.1:3001/api/books/unavailable
```

Consultar um livro inexistente:

```bash
curl -i -X GET \
  http://127.0.0.1:3001/api/books/999
```

Consultar um identificador inválido:

```bash
curl -i -X GET \
  http://127.0.0.1:3001/api/books/abc
```

### POST

Criar um novo livro

```bash
curl -i -X POST \
  -H "Content-Type: application/json" \
  -d '{"title":"Capitães da Areia","author":"Jorge Amado", "description": "Capitães da Areia de Jorge Amado", "year":1937,"available":true}' \
  http://127.0.0.1:3001/api/books
```

Tentar criar um livro com JSON malformado:

```bash
curl -i -X POST \
  -H "Content-Type: application/json" \
  -d '{"title":"Livro"' \
  http://127.0.0.1:3001/api/books
```

### PUT

Atualizar livros existentes

```bash
curl -i -X PUT \
  -H "Content-Type: application/json" \
  -d '{"title":"Capitães da Areia","author":"Jorge Amado", "description": "Capitães da Areia de Jorge Amado", "year":1937,"available":false}' \
  http://127.0.0.1:3001/api/books/3
```

Tentar atualizar um livro inexistente:

```bash
curl -i -X PUT \
  -H "Content-Type: application/json" \
  -d '{"title":"Livro","author":"Autor","description": "Descrição","year":2026,"available":true}' \
  http://127.0.0.1:3001/api/books/999
```

### DELETE

Remover o livro criado:

```bash
curl -i -X DELETE \
  http://127.0.0.1:3001/api/books/3
```

Tentar remover um livro inexistente:

```bash
curl -i -X DELETE \
  http://127.0.0.1:3001/api/books/999
```

### GET para confirmar remoção

Ao consultar a coleção novamente, o livro de identificador `3` não deve mais aparecer na resposta:

```bash
curl -i -X GET \
  http://127.0.0.1:3001/api/books
```
