# gunicorn_conf.py

import multiprocessing
import os

# Utiliza un socket UNIX para la comunicación
from multiprocessing import cpu_count

bind = "unix:/var/www/admisiones/admisiones.sock"

# Número de procesos de trabajo, generalmente se recomienda 2 * número de CPUs + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Puedes ajustar estos valores según tus necesidades
worker_class = "gthread"  # Puedes usar "sync", "gevent", etc.
threads = 2  # Número de hilos por proceso de trabajo
timeout = 30  # Tiempo de espera para las conexiones inactivas en segundos

# Configuración de registro
accesslog = '/home/logs/flask_access_admisiones.log'
errorlog = '/home/logs/flask_error_admisiones.log'
loglevel = "debug"  # Niveles posibles: debug, info, warning, error, critical
