from flask import Flask, render_template, request, redirect, abort

from mmmpaste import db
from mmmpaste.forms import NewPaste

app = Flask(__name__)

@app.teardown_request
def shutdown_session(exception = None):
    db.session.remove()

@app.route("/")
def root():
    pass

@app.route("/p/<id>")
def get_paste(id):
    paste = db.get_paste(id)
    if paste is None:
        abort(404)
    return render_template("paste.html", paste = paste)

@app.route("/history")
def history():
    pass

@app.route("/about")
def about():
    pass
