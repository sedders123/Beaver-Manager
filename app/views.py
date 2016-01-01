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
    inline_models = (EmergencyContact,)  # comma needed for some reason

    def on_model_change(self, form, model, is_created):
        badges = db.session.query(Badge).all()
        for badge in badges:
            beaver_badges = []
            for badge in model.badges:
                beaver_badges.append(badge.badge_id)
            if badge.id not in beaver_badges:
                beaver_badge = BeaverBadge(model.id, badge.id, False)
                db.session.add(beaver_badge)
                db.session.commit()
                print("Created Badge")

                for criterion in badge.criteria:
                    badge_id = model.id
                    badge_criterion = BadgeCriterion(criterion.id, badge_id, False)
                    db.session.add(badge_criterion)
                    db.session.commit()
                    print("Criterion Created")
            else:
                print("Badge not created")


class BadgeModelView(ModelView):
    inline_models = (Criterion,)

    def on_model_change(self, form, model, is_created):
        beavers = db.session.query(Beaver).all()
        for beaver in beavers:
            beaver_badges = []
            for badge in beaver.badges:
                beaver_badges.append(badge.badge_id)
            if model.id not in beaver_badges:
                beaver_badge = BeaverBadge(beaver.id, model.id, False)
                db.session.add(beaver_badge)
                db.session.commit()
                print("Created Badge")

                for criterion in model.criteria:
                    #badge = db.session.query(Badge).filter(Badge.beaver_id == beaver.id).all()  # list containing badge
                    badge_id = beaver_badge.id  # badge[0].id
                    badge_criterion = BadgeCriterion(criterion.id, badge_id, False)
                    db.session.add(badge_criterion)
                    db.session.commit()
                    print("Criterion Created")
            else:
                print("Badge not created")
# Debugging only
class BeaverBadgeModelView(ModelView):
        inline_models = (BadgeCriterion,)


admin.add_view(BeaverModelView(Beaver, db.session))
admin.add_view(BadgeModelView(Badge, db.session))
admin.add_view(ModelView(Lodge, db.session))
admin.add_view(ModelView(Trip, db.session))
admin.add_view(ModelView(Attendance, db.session))

admin.add_view(ModelView(Criterion, db.session, category='Debugging'))  # Debugging only
admin.add_view(ModelView(BadgeCriterion, db.session, category='Debugging'))  # Debugging only
admin.add_view(BeaverBadgeModelView(BeaverBadge, db.session, category='Debugging'))  # Hopefully debugging only
admin.add_view(ModelView(BeaverTrip, db.session, category='Debugging'))  # Hopefully debugging only
admin.add_view(ModelView(BeaverAttendance, db.session, category='Debugging'))  # Hopefully debugging only
