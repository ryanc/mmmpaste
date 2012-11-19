"""
A Flask paste bin.
"""

__author__ = 'Ryan Cavicchioni'
__license__ = 'BSD'

from flask import Flask
app = Flask(__name__, instance_relative_config = True)

app.config.from_object("mmmpaste.default_settings")
app.config.from_pyfile("application.cfg", silent = True)

import mmmpaste.views
