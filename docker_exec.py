from flask import Blueprint, request, current_app
from docker.errors import NotFound as ContainerNotFoundException
from werkzeug.exceptions import BadRequest, InternalServerError, Unauthorized, Forbidden

REQUIRED_KEYS = ["container", "exec"]
HEADER_AUTH_TOKEN = "x-auth-token"

docker_exec = Blueprint(__name__, __name__)

@docker_exec.post("/")
def post_docker_exec():
    req_json = request.get_json()

    if req_json is None:
        raise BadRequest("JSON required")

    for required_key in REQUIRED_KEYS:
        if required_key not in req_json.keys():
            raise BadRequest(f"{REQUIRED_KEYS} are required")

    container_name = req_json["container"]
    command = req_json["exec"]
    response = {"output": None}

    try:
        container = current_app.docker.containers.get(container_name)
        exit_code, output = container.exec_run(command)
        output = output.decode("utf-8")

        if exit_code != 0:
            raise InternalServerError(f"command returned {exit_code}: {output}")

        response["output"] = output

    except ContainerNotFoundException as e:
        raise BadRequest(f"container {container_name} not found")

    return response, 200

@docker_exec.before_request
def auth_middleware():
    if current_app.auth_token is None:
        return None

    # Headers should be case-insensitive
    headers = dict()
    for header, val in request.headers.items():
        headers[header.lower()] = val

    if HEADER_AUTH_TOKEN not in headers.keys():
        raise Unauthorized("an api key is required")

    if headers[HEADER_AUTH_TOKEN] != current_app.auth_token:
        raise Forbidden("api key invalid")

    return None
