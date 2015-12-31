from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

"""
A Managment system for Beavers

"""


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


from app import views, models

admin = Admin(app, name='beavermanager', template_mode='bootstrap3')
admin.add_view(ModelView(models.Beaver, db.session))
admin.add_view(ModelView(models.Badge, db.session))
admin.add_view(ModelView(models.MasterBadge, db.session))
admin.add_view(ModelView(models.Criterion, db.session))
admin.add_view(ModelView(models.MasterCriterion, db.session))
admin.add_view(ModelView(models.Lodge, db.session))
