# gunicorn.conf.py
import multiprocessing
import os

# Server socket - use Render's PORT
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"