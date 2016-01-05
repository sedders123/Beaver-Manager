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
    sort_form = SortForm()
    return render_template("beavers.html", beavers=beavers, form=sort_form)


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
    beaver_attendances = BeaverAttendance.query.all()
    selected = []

    class ChoiceObj(object):
        def __init__(self, name, choices):
            """
              This is needed so that BaseForm.process will accept the object for the named form,
              and eventually it will end up in SelectMultipleField.process_data and get assigned
              to .data
            """
            setattr(self, name, choices)
    for beaver_attendance in beaver_attendances:
        selected.append(beaver_attendance.beaver_id)

    selectedChoices = ChoiceObj('beavers', selected )
    form = BeaverAttendanceForm(obj=selectedChoices)
    form.beavers.choices = []


    for beaver in beavers:
        name = beaver.first_name + " " + beaver.surname
        choice = (beaver.id, name)
        form.beavers.choices.append(choice)

    if form.validate_on_submit():
        print("Whoop",form.__dict__.keys())
        present = form.beavers.data
        print(present)
        print(selected)
        for beaver_id in present:
            if beaver_id not in selected:
                beaver_attendance = BeaverAttendance(attendance_id, beaver_id,
                                                     True)
                db.session.add(beaver_attendance)
                db.session.commit()
        for beaver_id in selected:
            if (beaver_id not in present) and (beaver_id in selected):
                print(beaver_id)
                beaver_attendance = BeaverAttendance.query.filter_by(beaver_id=beaver_id,attendance_id=attendance_id).all()
                db.session.delete(beaver_attendance[0])  # needs index as query returns a list
                db.session.commit()
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
