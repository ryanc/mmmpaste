from flask import Blueprint, abort, make_response, request, url_for

from mmmpaste import db, filters

rest = Blueprint("rest", __name__)


@rest.teardown_request
def shutdown_session(exception = None):
    db.session.remove()


@rest.route("/api/paste", methods = ["POST"])
def new_paste():
    id = db.new_paste(request.form.get("content"),
                      request.remote_addr,
                      request.form.get("filename", None),
                      request.form.get("highlight", True),
                      request.form.get("convert_tabs", True))

    response = make_response("", 201)
    response.headers["Location"] = url_for("get_paste", id = id)
    return response


@rest.route("/api/paste/<id>", methods = ["GET"])
@filters.cache
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
