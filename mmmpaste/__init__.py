"""
A Flask paste bin.
"""

__author__ = 'Ryan Cavicchioni'
__license__ = 'BSD'

from flask import Flask

app = Flask(__name__)

# Import the default settings.
app.config.from_object('mmmpaste.settings')

import mmmpaste.views
