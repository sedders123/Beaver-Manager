from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import InlineFormAdmin
from flask_admin import Admin

from app import app, db
from .models import *
from .views import *
from .forms import *

admin = Admin(app, name='beavermanager', template_mode='bootstrap3')


@app.route('/')
@app.route('/index')
def index():
    """Displays the homepage"""
    return render_template("index.html",title='Home')


@app.route('/beavers')
def beavers():
    """Queries the database for all beavers then displays a list of them"""
    beavers = Beaver.query.all()
    return render_template("beavers.html", beavers=beavers)


@app.route('/beavers/<beaver_id>')
def beaver_individual(beaver_id):
    """Displays Information about  the given beaver"""
    beaver = Beaver.query.get(beaver_id)
    return render_template("beaver.html", beaver=beaver)


@app.route('/registers')
def register_main():
    """Displays which dates registers can be taken upon"""
    attendances = Attendance.query.all()
    return render_template("register_main.html", attendances=attendances)


@app.route('/registers/<attendance_id>', methods=['GET', 'POST'])
def register_beavers(attendance_id):
    """Displays a form to record beaver atendance"""
    beavers = Beaver.query.all()
    form = BeaverAttendanceForm()
    if form.validate_on_submit():
        print(form.__dict__.keys())
    return render_template("register.html", beavers=beavers, form=form)

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
                    badge_criterion = BadgeCriterion(criterion.id, badge_id,
                                                     False)
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
                    badge_id = beaver_badge.id  # badge[0].id
                    badge_criterion = BadgeCriterion(criterion.id, badge_id,
                                                     False)
                    db.session.add(badge_criterion)
                    db.session.commit()
                    print("Criterion Created")
            else:
                print("Badge not created")


class TripModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        beavers = db.session.query(Beaver).all()
        for beaver in beavers:
            beaver_trips = []
            for trip in beaver.trips:
                beaver_trips.append(trip.trip_id)
            if model.id not in beaver_trips:
                beaver_trip = BeaverTrip(beaver.id, model.id, False, False)
                db.session.add(beaver_trip)
                db.session.commit()
                print("BeaverTrip Created")
            else:
                print("BeaverTrip not created")


class AttendanceModelView(ModelView):
    inline_models = (BeaverAttendance,)


# Debugging only
class BeaverBadgeModelView(ModelView):
    inline_models = (BadgeCriterion,)


admin.add_view(BeaverModelView(Beaver, db.session))
admin.add_view(BadgeModelView(Badge, db.session))
admin.add_view(ModelView(Lodge, db.session))
admin.add_view(TripModelView(Trip, db.session))
admin.add_view(AttendanceModelView(Attendance, db.session))

admin.add_view(ModelView(Criterion, db.session, category='Extra'))
admin.add_view(ModelView(BadgeCriterion, db.session, category='Extra'))
admin.add_view(BeaverBadgeModelView(BeaverBadge, db.session, category='Extra'))
admin.add_view(ModelView(BeaverTrip, db.session, category='Extra'))
admin.add_view(ModelView(BeaverAttendance, db.session, category='Extra'))
