"""
This file contains the configuration for the Flask application.
"""

from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

# Load env for db connection
load_dotenv(path.join(basedir, ".env-postgresql"))

DB_NAME = environ.get("POSTGRES_DB")
DB_USER = environ.get("POSTGRES_USER")
DB_PASSWORD = environ.get("POSTGRES_PASSWORD")
DB_HOST = environ.get("DATABASE_HOST")
DB_PORT = environ.get("DATABASE_PORT")
