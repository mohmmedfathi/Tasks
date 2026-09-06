# Online Book Store

## Design Decisions

- **Authentication:** SimpleJWT handles login and token refresh. Refresh tokens
  rotate and used tokens are blacklisted to prevent replay
- **Cursor pagination:** Book and review lists use cursor pagination because it
  stays stable when new records are added. The ID is a tie breaker when values
  are equal
- **Database rules:** PostgreSQL constraints keep ratings between 1 and 5 and
  allow one review per user for each book
- **Concurrent requests:** Review creation uses an atomic transaction. The
  database rejects duplicate reviews even when two requests arrive together
- **Query performance:** Book lists do not load the large content field. Review
  statistics are calculated by PostgreSQL. Review queries load users in the same
  query to avoid extra database calls
- **Tests:** Pytest covers API behavior and permissions against PostgreSQL
- **API documentation:** drf-spectacular generates the OpenAPI schema and
  Swagger UI

## Run the Project

Docker Desktop is required

Start Django and PostgreSQL:

```bash
docker compose up --build -d
```

Load the sample books:

```bash
docker compose exec web python manage.py loaddata books
```

The API is available at `http://localhost:8000`

- Swagger UI: `http://localhost:8000/api/docs/`

## Run with pip

Start only PostgreSQL in Docker and run Django on your machine:

```bash
docker compose up -d db
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata books
python manage.py runserver
```
## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/auth/register/` | Register a user |
| `POST` | `/api/auth/login/` | Get access and refresh tokens |
| `POST` | `/api/auth/refresh/` | Rotate the refresh token |
| `POST` | `/api/auth/logout/` | Blacklist a refresh token |
| `GET` | `/api/books/` | List books |
| `GET` | `/api/books/{id}/` | Get book details and content |
| `GET` | `/api/books/{id}/reviews/` | List reviews for a book |
| `POST` | `/api/books/{id}/reviews/` | Create a review |
| `PATCH` | `/api/reviews/{id}/` | Update your review |
| `DELETE` | `/api/reviews/{id}/` | Delete your review |

Book and review endpoints require `Authorization: Bearer <access_token>`
List endpoints accept an optional `limit` query parameter


## Run Tests

Install the development dependencies in the running container then run pytest:

```bash
docker compose exec web uv sync --frozen
docker compose exec web pytest --cov=. --cov-report=term-missing
```

