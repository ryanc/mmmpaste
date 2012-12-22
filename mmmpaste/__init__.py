from flask import Flask

app = Flask(__name__)

# Import the default settings.
app.config.from_object('mmmpaste.settings')

import mmmpaste.views
