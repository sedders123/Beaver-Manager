from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.orm import model_form
from .models import Beaver
from app import db

BeaverForm = model_form(Beaver, db_session=db.session, base_class=Form)
