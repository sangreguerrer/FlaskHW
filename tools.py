from schema import SCHEMA_MODEL
from pydantic import ValidationError
from errors import HttpError
from flask import jsonify
from app import get_app


app = get_app()


def get_json_response(data: dict, status_code=200):
    return jsonify(data), status_code


def handle_error(error: HttpError):
    return get_json_response(
        {"status": "error", "description": error.description}, error.status_code
    )


def validate(model: SCHEMA_MODEL, data: dict):
    try:
        return model.model_validate(data).model_dump(exclude_unset=True)
    except ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)