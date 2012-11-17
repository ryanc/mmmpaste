import json
from functools import wraps

from flask import Blueprint, abort, make_response, request, url_for, current_app

from mmmpaste import db, filters, helpers

rest = Blueprint("rest", __name__)


@rest.teardown_request
def shutdown_session(exception = None):
    db.session.remove()


def check_auth(user, password):
    config = current_app.config

    if "ADMIN_PASSWORD" not in config:
        return False

    return user == 'admin' and password == config.get("ADMIN_PASSWORD")


def authenticate():
    response = make_response("", 401)
    response.headers["WWW-Authenticate"] = 'Basic realm="Mmm Paste"'
    return response


def requires_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return fn(*args, **kwargs)
    return wrapper


@rest.route("/paste", methods = ["POST"])
def new_paste():
    id = db.new_paste(request.form.get("content"),
                      helpers.get_ip(),
                      request.form.get("filename", None),
                      request.form.get("highlight", True),
                      request.form.get("convert_tabs", True))

    response = json_response({"id": id}, 201)
    response.headers["Location"] = url_for("get_paste", id = id)
    return response


@rest.route("/paste/<id>", methods = ["GET"])
@filters.cache
@filters.runtime
def get_paste(id):
    paste = db.get_paste(id)

    if paste is None:
        return json_error("Paste not found.", 404)

    response = make_response(str(paste.content))
    response.mimetype = "text/plain"
    return response


@rest.route("/paste/<id>", methods = ["DELETE"])
@requires_auth
def delete_paste(id):
    db.deactivate_paste(id)
    return "", 204


def json_error(message, status_code):
    return json_response({'error': message}, status_code)


def json_response(obj, status_code = 200):
    text = json.dumps(obj) + "\n"
    response = make_response(text, status_code)
    response.headers["Content-Type"] = "application/json"
    return response
