import multiprocessing

# Gunicorn configuration file
bind = "0.0.0.0:10000"
workers = 2
worker_class = "sync"
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True
enable_stdio_inheritance = True
