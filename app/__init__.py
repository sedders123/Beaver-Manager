from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

"""
A Managment system for Beavers

"""


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


from app import views, models
