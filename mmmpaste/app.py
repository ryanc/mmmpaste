from flask import Flask

from mmmpaste import db

app = Flask(__name__)

@app.teardown_request
def shutdown_session(exception = None):
    db.session.remove()

@app.route("/")
def root():
    return "Nothing to see here, move along."
