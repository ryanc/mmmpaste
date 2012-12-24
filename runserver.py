import os

from mmmpaste import app

PORT = int(os.environ['PORT']) if 'PORT' in os.environ else 5000

app.run(debug = True, port = PORT)
