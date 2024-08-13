import os
from dotenv import load_dotenv
from urllib.parse import quote

from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    # verification de que si existe el archivo .env
    if not os.path.exists(env_path):
        raise Exception("No se ha encontrado el archivo .env")

    # verification de que si se cargaron las variables de entorno
    assert os.getenv("APLICACION"), "No se ha definido la variable de entorno APLICACION"
    assert os.getenv("VERSION"), "No se ha definido la variable de entorno VERSION"
    assert os.getenv("SECRET_KEY"), "No se ha definido la variable de entorno SECRET_KEY"
    assert os.getenv("DEBUG"), "No se ha definido la variable de entorno DEBUG"
    assert os.getenv("ALLOWED_HOSTS"), "No se ha definido la variable de entorno ALLOWED_HOSTS"

    # datos generales
    APP_NAME: str = os.getenv("APLICACION")
    APP_VERSION: str = os.getenv("VERSION")
    APP_IP: str = os.getenv("APP_IP")
    HOST: str = os.getenv("HOST")
    PORT: str = os.getenv("PORT")
    SERVER_NAME: str = os.getenv("SERVER_NAME")
    ALLOWED_HOSTS: str = os.getenv("ALLOWED_HOSTS")
    HTTPS: bool = os.getenv("HTTPS")

    # connexion con mysql
    DB_NAME: str = os.getenv("DB_NAME_MYSQL")
    DB_USER: str = os.getenv("DB_USER_MYSQL")
    DB_PASS: str = os.getenv("DB_PASS_MYSQL")
    DB_HOST: str = os.getenv("DB_HOST_MYSQL")
    DB_PORT: str = os.getenv("DB_PORT_MYSQL")
    DB_DNS: str = os.getenv("DB_DNS_MYSQL")
    escaped_DB_PASS = quote(str(DB_PASS), safe='')
    DATABASE_URL = f"mysql://{DB_USER}:{escaped_DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # log files y static files
    LOG_FILES_URL: str = os.getenv("LOG_FILES_URL")
    STATIC_FILES_URL: str = os.getenv("STATIC_URL")
    PREFIX_URL: str = os.getenv("PREFIX_URL")
    SUFIX_URL: str = os.getenv("SUFIX_URL")

    # variables de entorno
    DEBUG: bool = os.getenv("DEBUG")

    # flask security
    SECRET_KEY: str = os.getenv("SECRET_KEY")


config = Config()
