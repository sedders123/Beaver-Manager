from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db
from .models import Beaver


@app.route('/')
@app.route('/index')
def index():
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
    Beavers = Beaver.query.order_by(Beaver.surname)
    return render_template("beavers.html", beavers=Beavers)


@app.route('/new_beaver')
def new_beaver():
    form = NewBeaverForm()
