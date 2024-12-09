FROM python:3.12 AS builder

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.5.1 /uv /uvx /bin/

COPY requirements.lock .
RUN uv venv /opt/venv && \
    uv pip install --no-cache -r requirements.lock

# run stage
FROM python:3.12-slim-bookworm

RUN apt-get -y update && \
    apt-get install -y ffmpeg &&\
    apt-get -y update && \
    apt-get clean all

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . .

CMD ["/bin/bash", "-c", "alembic upgrade heads;python -m app.consumer"]