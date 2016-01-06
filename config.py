"""
Contains the configuration options for the flask app.

Attributes:
    basedir (str): Base directory of the flask app
    SQLALCHEMY_DATABASE_URI (str): Location of SQLAlchemy database
    SQLALCHEMY_MIGRATE_REPO (str): Directory containg databae migrations and
                                   history
    WTF_CSRF_ENABLED (bool): Whether CSRF is enable for forms, protecting data
    SECRET_KEY (str): A secret key
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
