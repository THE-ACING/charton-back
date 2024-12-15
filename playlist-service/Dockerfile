FROM python:3.13 AS builder

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.5.1 /uv /uvx /bin/

COPY requirements.lock .
RUN uv venv /opt/venv && \
    uv pip install --no-cache -r requirements.lock

# run stage
FROM python:3.13-slim-bookworm

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . .

EXPOSE 50051
CMD ["/bin/bash", "-c", "alembic upgrade heads;python -m app.server"]