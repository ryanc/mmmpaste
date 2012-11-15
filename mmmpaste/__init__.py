from flask import Flask
app = Flask(__name__, instance_relative_config = True)

app.config.from_object("mmmpaste.default_settings")
app.config.from_object("local_settings")

import mmmpaste.views
