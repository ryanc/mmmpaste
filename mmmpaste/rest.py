from flask import Blueprint, abort, make_response, request, url_for

from mmmpaste import db

rest = Blueprint("rest", __name__)


@rest.teardown_request
def shutdown_session(exception = None):
    db.session.remove()


@rest.route("/api/paste", methods = ["POST"])
def new_paste():
    content = request.form.get("content")
    filename = request.form.get("filename", None)
    highlight = request.form.get("highlight", True)
    convert_tabs = request.form.get("convert_tabs", True)

    id = db.new_paste(content, request.remote_addr, filename, highlight,
                      convert_tabs)

    response = make_response("", 201)
    response.headers["Location"] = url_for(".get_paste", id = id)
    return response


@rest.route("/api/paste/<id>", methods = ["GET"])
def get_paste(id):
    paste = db.get_paste(id)

    if paste is None or paste.is_active is False:
        abort(404)

    response = make_response(str(paste.content))
    response.mimetype = "text/plain"
    return response


@rest.route("/api/paste/<id>", methods = ["DELETE"])
def delete_paste(id):
    #db.deactivate_paste(id)
    return "", 204
