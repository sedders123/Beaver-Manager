from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db
from .models import Beaver
from .views import *

"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the routing paths used by Flask to render pages that the user requests. Also includes logic used to parse information in and out of templates


"""


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
