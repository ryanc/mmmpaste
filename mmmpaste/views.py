from flask import Flask, render_template, request, redirect, abort, url_for, \
                  make_response, session, flash

from mmmpaste import app
from mmmpaste import db
from mmmpaste import forms
from mmmpaste import filters
from mmmpaste.rest import rest

from functools import update_wrapper

# Register the REST API module.
app.register_blueprint(rest)


@app.teardown_request
def shutdown_session(exception = None):
    db.session.remove()


@app.errorhandler(404)
def page_not_found(e):
    error = "Page not found :("
    return render_template("error.html", error = error), 404


@app.errorhandler(500)
def page_not_found(e):
    error = "The system is down. The system is down."
    return render_template("error.html", error = error), 500


@app.route("/")
def root():
    return redirect(url_for("new_paste"))


@app.route("/p/<id>")
@filters.cache
def get_paste(id):
    paste = db.get_paste(id)

    if paste is None or paste.is_active is False:
        error = "This paste is no longer available."
        return render_template("error.html", error = error), 404

    return render_template("paste.html", paste = paste)


@app.route("/new", methods = ["POST", "GET"])
@filters.no_cache
def new_paste():
    form = forms.NewPaste(request.form)
    if request.method == "POST" and form.validate():
        id = db.new_paste(form.content.data, request.remote_addr,
                          form.filename.data, form.highlight.data,
                          form.convert_tabs.data)
        if "pastes" not in session:
            session["pastes"] = []

        pastes = session["pastes"]
        pastes.append(id)
        session["paste"] = pastes

        return redirect(url_for("get_paste", id = id))

    return render_template("new.html", form = form)


@app.route("/history")
def history():
    pass


@app.route("/about")
def about():
    pass


@app.route("/p/<id>/raw")
@filters.cache
def get_raw_paste(id):
    paste = db.get_paste(id)

    if paste is None or paste.is_active is False:
        error = "This paste is no longer available."
        return render_template("error.html", error = error), 404

    response = make_response(str(paste.content))
    response.mimetype = "text/plain"
    return response


@app.route("/p/<id>/download")
@filters.cache
def download_paste(id):
    paste = db.get_paste(id)

    if paste is None or paste.is_active is False:
        error = "This paste is no longer available."
        return render_template("error.html", error = error), 404

    filename = paste.filename

    if filename is None:
        filename = "paste-%s.txt" % paste.id_b62

    response = make_response(str(paste.content))
    response.headers["Content-Disposition"] = "attachment; filename=%s" % filename
    return response


@app.route("/p/<id>/clone")
def clone_paste(id):
    paste = db.get_paste(id)

    if paste is None or paste.is_active is False:
        error = "This paste is no longer available."
        return render_template("error.html", error = error), 404

    form = forms.NewPaste()
    form.content.data = str(paste.content)
    return render_template("new.html", form = form)


@app.route("/p/<id>/delete")
def delete_paste(id):
    if id not in session["pastes"]:
        error = "You do not have permission to delete this paste."
        return render_template("error.html", error = error), 403

    db.deactivate_paste(id)
    flash("The paste has been deleted.")
    return redirect(url_for("new_paste"))


@app.route("/latest")
def get_latest_paste():
    paste = db.get_paste()
    return redirect(url_for("get_paste", id = paste.id_b62), 307)
