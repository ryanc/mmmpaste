import os

from mmmpaste import app

# Get the port from the enviroment or fall back to the default.
PORT = int(os.environ.get('PORT', 5000))

app.run(debug = True, port = PORT)
