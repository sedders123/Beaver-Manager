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
import passwords as passwords
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

PUSHER_APP_ID = "165123"
PUSHER_KEY = "00ded34053ebced28ff5"
PUSHER_SECRET = "3feabf30f6c57931afe5"


MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = passwords.mail_username
MAIL_PASSWORD = passwords.mail_password
