import json

from flask import Blueprint, abort, make_response, request, url_for

from mmmpaste import db, filters

rest = Blueprint("rest", __name__)


@rest.teardown_request
def shutdown_session(exception = None):
    db.session.remove()


@rest.route("/paste", methods = ["POST"])
def new_paste():
    id = db.new_paste(request.form.get("content"),
                      request.remote_addr,
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

    if paste is None or paste.is_active is False:
        return json_error("Paste not found.", 404)

    response = make_response(str(paste.content))
    response.mimetype = "text/plain"
    return response


@rest.route("/paste/<id>", methods = ["DELETE"])
def delete_paste(id):
    #db.deactivate_paste(id)
    return "", 204


def json_error(message, status_code):
    return json_response({'error': message}, status_code)


def json_response(obj, status_code = 200):
    text = json.dumps(obj) + "\n"
    response = make_response(text, status_code)
    response.headers["Content-Type"] = "application/json"
    return response
