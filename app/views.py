from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

from app import app, db
from .models import *
from .views import *

"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the routing paths used by Flask to render pages that the user requests. Also includes logic used to parse information in and out of templates


"""

admin = Admin(app, name='beavermanager', template_mode='bootstrap3')

@app.route('/')
@app.route('/index')
def index():
    """Displays the homepage"""
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/beavers')
def beavers():
    """Queries the database for all beavers then displays a list of them"""
    Beavers = Beaver.query.all()
    return render_template("beavers.html", beavers=Beavers)


class BeaverModelView(ModelView):
    inline_models=(EmergencyContact,) # comma needed for some reason


class MasterBadgeModelView(ModelView):
    inline_models=(MasterCriterion,)


class BadgeModelView(ModelView):
        inline_models=(Criterion,)


admin.add_view(BeaverModelView(Beaver, db.session))
admin.add_view(BadgeModelView(Badge, db.session))
admin.add_view(MasterBadgeModelView(MasterBadge, db.session))
admin.add_view(ModelView(Criterion, db.session))
admin.add_view(ModelView(MasterCriterion, db.session))
admin.add_view(ModelView(Lodge, db.session))
