from flask import Flask, render_template, request, redirect, url_for
from config import Config
import logging

# Localizacion de los logs generados por Flask
LOG_FILENAME = str(Config.LOG_FILES_URL)
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# prefijo de ruta necesario para las rutas
PREFIX = str(Config.PREFIX_URL)
SUFIX = str(Config.SUFIX_URL)

# configuracion de la aplicacion
app = Flask(__name__)
app.config['SECRET_KEY'] = str(Config.SECRET_KEY)
app.config['APPLICATION_ROOT'] = str(Config.PREFIX_URL)
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

# define the base path for templates
BASE_PAGES = "pages"

# logging del server name
logging.info('Nombre del servidor: %s', app.config['SERVER_NAME'])
logging.info('Prefijo de la aplicacion: %s', app.config['APPLICATION_ROOT'])
# logging de los host permitidos
logging.info('Hosts permitidos: %s', Config.ALLOWED_HOSTS)

# limpia la url para evitar problemas
@app.before_request
def add_trailing_slash():
    if not request.path.lower().endswith('/') and SUFIX != '':
        return redirect(request.path.lower() + '/')

# registra variables globales al contexto de los templates
@app.context_processor
def inject_user():
    return dict(prefix=PREFIX, sufix=SUFIX, debug=Config.DEBUG)