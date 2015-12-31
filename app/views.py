from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db
from .models import Beaver
from .views import *


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
    Beavers = Beaver.query.all()
    return render_template("beavers.html", beavers=Beavers)


@app.route('/new_beaver')
def new_beaver():
    form = NewBeaverForm()


@app.route("/edit<id>", methods=['GET', 'POST'])
def edit(id):
    beaver = db.session.query(Beaver).filter(Beaver.id == id)
    form = BeaverForm(obj=beaver)

    if form.validate_on_submit():
        form.populate_obj(beaver[0])
        for beaver_actual in beaver:
            beaver_actual.save()
        flash("Beaver updated")
        return redirect(url_for("index"))
    return render_template("edit_beaver.html", form=form, action="Edit", data_type="a beaver")


@app.route("/add_beaver", methods=['GET', 'POST'])
def add():
    form = BeaverForm(request.form)

    if form.validate_on_submit():
        beaver = Beaver()
        form.populate_obj(beaver)
        db.session.add(beaver)
        db.session.commit()
        flash("Beaver added")
        return redirect(url_for("index"))
    return render_template("edit_beaver.html", form=form, action="Add")
