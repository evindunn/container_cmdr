#!/usr/bin/env python3

from json import dumps as json_dumps
from logging import basicConfig as loggerBasicConfig, INFO
from os import getenv

from docker import from_env as docker_from_env
from flask import Flask
from werkzeug.exceptions import HTTPException
from docker_exec import docker_exec

LOG_FMT = "[%(asctime)s][%(levelname)s] %(message)s"
LOG_DATE_FMT = "%Y-%m-%dT%H:%M:%S%z"
LOG_LEVEL = INFO
ENV_AUTH_TOKEN = "AUTH_TOKEN"


def on_http_exception(e: HTTPException):
    response = e.get_response()
    response.content_type = "application/json"
    response.data = json_dumps({
        "error": e.description
    })
    return response


def create_app():
    loggerBasicConfig(
        format=LOG_FMT,
        datefmt=LOG_DATE_FMT,
        level=LOG_LEVEL
    )

    app = Flask(__name__)
    app.docker = docker_from_env()
    app.auth_token = getenv(ENV_AUTH_TOKEN, None)

    app.register_blueprint(docker_exec)
    app.register_error_handler(HTTPException, on_http_exception)

    return app
