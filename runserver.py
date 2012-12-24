import os

from mmmpaste import app

# Get the port from the enviroment or fall back to the default.
PORT = int(os.environ.get('PORT', 5000))
DEBUG = bool(os.environ.get('PORT', True))

app.run(debug = DEBUG, port = PORT)
