bind = "unix:run/app.sock"
umask = 0177
accesslog = "log/gunicorn.access.log"
errorlog = "log/gunicorn.error.log"
workers = 3
