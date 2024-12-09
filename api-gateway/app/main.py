import logging

import logfire
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from app.factory import create_app
from app.settings import SettingsProvider
from app.utils import GrpcProvider

logfire.configure(service_name="api-gateway")
logging.basicConfig(level=logging.INFO, handlers=[logfire.LogfireLoggingHandler()])

app = create_app()
logfire.instrument_fastapi(app)

container = make_async_container(SettingsProvider(), GrpcProvider())
setup_dishka(container=container, app=app)