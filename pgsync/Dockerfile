FROM python:3.13 as builder

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.5.1 /uv /uvx /bin/

RUN uv venv /opt/venv && \
    uv pip install git+https://github.com/toluaina/pgsync.git

FROM python:3.13-slim-bookworm

ARG WORKDIR=/code
WORKDIR $WORKDIR

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

# Ensure scripts are executable
RUN chmod +x entrypoint.sh
RUN chmod +x wait-for-it.sh

ENTRYPOINT ["./entrypoint.sh"]
