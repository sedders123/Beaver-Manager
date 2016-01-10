"""
Beaver Management app using flask

Attributes:
    app (:class:`Flask<flask:flask.Flask>`): Flask application instance
    db (:class:`SQLAlchemy<sqla:flask.ext.sqlalchemy.SQLAlchemy>`): SQLAlchemy
                                                               databse instance
"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.logger.setLevel('INFO')


from beaver_manager import views, models
