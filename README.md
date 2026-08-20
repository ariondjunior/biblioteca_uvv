# API - Catálogo de Livros

Servidor HTTP simples para gerenciar um catálogo de livros em memória. A
implementação utiliza somente a biblioteca padrão do Python.

## Executar

Em um terminal, execute:

```bash
python3 biblioteca_server.py
```

O servidor ficará disponível em `http://127.0.0.1:3001`.

## Modelagem

A documentação dos recursos, URIs, métodos, códigos de status e comandos para
a apresentação está em [modelagem.md](modelagem.md).

## Testes com curl

Execute os comandos abaixo em outro terminal, com o servidor em execução.

```bash
# Listar livros
curl -i http://127.0.0.1:3001/api/books

# Consultar um livro existente
curl -i http://127.0.0.1:3001/api/books/1

# Consultar um livro inexistente
curl -i http://127.0.0.1:3001/api/books/999

# Criar um livro
curl -i -X POST \
  -H "Content-Type: application/json" \
  -d '{"title":"Capitães da Areia","author":"Jorge Amado","description":"Romance de Jorge Amado","year":1937,"available":true}' \
  http://127.0.0.1:3001/api/books

# Atualizar um livro
curl -i -X PUT \
  -H "Content-Type: application/json" \
  -d '{"title":"Dom Casmurro","author":"Machado de Assis","description":"Romance realista de Machado de Assis","year":1899,"available":false}' \
  http://127.0.0.1:3001/api/books/1

# Remover um livro
curl -i -X DELETE http://127.0.0.1:3001/api/books/2

# Identificador inválido
curl -i http://127.0.0.1:3001/api/books/abc

# JSON inválido
curl -i -X POST \
  -H "Content-Type: application/json" \
  -d '{"title":"Livro"' \
  http://127.0.0.1:3001/api/books

# Campo obrigatório ausente
curl -i -X POST \
  -H "Content-Type: application/json" \
  -d '{"title":"Livro","author":"Autor","description":"Descrição do livro","year":2026}' \
  http://127.0.0.1:3001/api/books

# Rota inexistente
curl -i http://127.0.0.1:3001/usuarios
```