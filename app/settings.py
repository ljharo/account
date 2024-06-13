# settings.py

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

SERVER_INFO: dict = {
    'app': 'app.apis:app',
    'host': os.environ.get('HOST'),
    'port': int(os.environ.get('PORT')),
    'reload': bool(int(os.getenv("DEBUG"))),
}

DB_URI: str = os.environ.get('DB_URI')

SECRET_KEY: str = os.environ.get('SECRET_KEY')

# Crear el engine
engine = create_engine(DB_URI)

# Crear la sesión
Session = sessionmaker(bind=engine)
session = Session()

# Definir la base
Base = declarative_base()