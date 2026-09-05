FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.17 /uv /bin/uv

WORKDIR /app
COPY . .
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"

CMD ["gunicorn", "--chdir", "src", "config.wsgi", "--bind", "0.0.0.0:8000"]
