from flask import Flask, render_template, request, redirect, abort, url_for, \
                  make_response

from mmmpaste import db
from mmmpaste import forms

app = Flask(__name__)

@app.teardown_request
def shutdown_session(exception = None):
    db.session.remove()


@app.route("/")
def root():
    return redirect(url_for("new_paste"))


@app.route("/p/<id>")
def get_paste(id):
    paste = db.get_paste(id)

    if paste is None:
        abort(404)

    return render_template("paste.html", paste = paste)


@app.route("/new", methods = ["POST", "GET"])
def new_paste():
    form = forms.NewPaste(request.form)
    if request.method == "POST" and form.validate():
        id = db.new_paste(form.content.data, form.filename.data,
                          form.highlight.data, form.convert_tabs.data)
        return redirect(url_for("get_paste", id = id))

    return render_template("new.html", form = form)


@app.route("/history")
def history():
    pass


@app.route("/about")
def about():
    pass


@app.route("/p/<id>/raw")
def get_raw_paste(id):
    paste = db.get_paste(id)

    if paste is None:
        return abort(404)

    response = make_response(str(paste.content))
    response.mimetype = "text/plain"
    return response


@app.route("/p/<id>/download")
def download_paste(id):
    paste = db.get_paste(id)

    if paste is None:
        return abort(404)

    filename = paste.filename

    if filename is None:
        filename = "paste-%s.txt" % paste.id_b62

    response = make_response(str(paste.content))
    response.headers["Content-Disposition"] = "attachment; filename=%s" % filename
    return response


@app.route("/p/<id>/clone")
def clone_paste(id):
    paste = db.get_paste(id)

    if paste is None:
        return abort(404)

    form = forms.NewPaste()
    form.content.data = str(paste.content)
    return render_template("new.html", form = form)


@app.route("/latest")
def get_latest_paste():
    paste = db.get_paste()
    return redirect(url_for("get_paste", id = paste.id_b62), 307)
