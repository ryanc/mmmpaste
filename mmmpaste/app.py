from flask import Flask

from mmmpaste import db
from mmmpaste.forms import NewPasteForm

app = Flask(__name__)

@app.teardown_request
def shutdown_session(exception = None):
    db.session.remove()

@app.route("/")
def root():
    pass

@app.route("/history")
def history():
    pass

@app.route("/about")
def about():
    pass
