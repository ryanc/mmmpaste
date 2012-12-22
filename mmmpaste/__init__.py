"""
A Flask paste bin.
"""

__author__ = 'Ryan Cavicchioni'
__license__ = 'BSD'

from flask import Flask

import settings

app = Flask(__name__)

app.config.from_object('mmmpaste.default_settings')
app.config.from_object(settings)

import mmmpaste.views
