"""
This module contains the views for the app.

Using flasks :class:`route()<flask:flask.Flask.route>` function to route the
request it then executes the nesecerrary code return a rendered template at
the end.
"""
from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import InlineFormAdmin
from flask_admin import Admin

from app import app, db
from .models import *
from .views import *
from .forms import *
from .logic import *

admin = Admin(app, name='beavermanager', template_mode='bootstrap3')


@app.route('/')
@app.route('/index')
def index():
    """Displays the homepage"""
    sort_form = SortForm()
    attendances = Attendance.query.all()
    for attendance in attendances:
        update_criterion(attendance)
        beaver_badges = BeaverBadge.query.all()
        for beaver_badge in beaver_badges:
            update_beaver_badge(beaver_badge)
    test = ""  #: Doc Can be used to print variables during runtime
    return render_template("index.html", html_title='Home', test=test)


@app.route('/beavers')
def beavers():
    """Queries the database for all beavers then displays a list of them"""
    beavers = Beaver.query.all()
    sort_form = SortForm()
    return render_template("beavers.html", beavers=beavers, form=sort_form)


@app.route('/beavers/<beaver_id>')
def beaver(beaver_id):
    """
    Displays Information about the given beaver

    Args:
        beaver_id (int): The ID number of the beaver record
    """
    beaver = Beaver.query.get(beaver_id)
    beaver_attendances = beaver.beaver_attendances
    total = 0
    present = 0
    absent = 0
    for beaver_attendance in beaver_attendances:
        total += 1
        if beaver_attendance.present:
            present += 1
        else:
            absent += 1
    present = to_percent(present, total)
    absent = to_percent(absent, total)
    # http://www.highcharts.com/demo/3d-pie
    # https://gist.github.com/vgoklani/5347161
    chartID = "chart_" + str(beaver.id)
    series = [{
              'type': 'pie',
              'name': 'Attendance',
              'colorByPoint': 'true',
              'data': [{
                        'name': 'Present',
                        'y': present
                       },
                       {
                        'name': 'Absent',
                        'y': absent
                       }]
              }]
    title = {'text': 'Attendance'}
    chart = {
                'renderTo': chartID,
                'type': 'pie',
                'plotBorderWidth': 'null',
                'plotShadow': 'false',
            }
    plot_options = {
                'pie': {
                        'allowPointSelect': 'true',
                        'cursor': 'pointer',
                        'dataLabels': '{'
                                      'enabled: false'
                                      '}',
                        'showInLegend': 'true'
                        }
                    }
    height = 40
    return render_template("beaver.html", beaver=beaver, chartID=chartID,
                           series=series, title=title, chart=chart,
                           plot_options=plot_options, height=height)


@app.route('/registers')
def registers():
    """Displays a list displaying dates for which registers can be taken"""
    attendances = Attendance.query.all()
    total_present = {}
    for attendance in attendances:
        total_present[attendance.id] = 0
        for beaver_attendance in attendance.beaver_attendances:
            if beaver_attendance.present:
                total_present[attendance.id] += 1
    return render_template("register_main.html", attendances=attendances,
                           total_present=total_present)


@app.route('/registers/<attendance_id>', methods=['GET', 'POST'])
def register(attendance_id):
    """
    Displays a form to record beavers atendance.

    Args:
        attendance_id (int): The ID number of the attendance record
    """
    beavers = Beaver.query.all()
    beaver_attendances = BeaverAttendance.query.filter_by(attendance_id=attendance_id).all()
    selected = []

    class ChoiceObj(object):
        def __init__(self, name, choices):
            """
              This is needed so that BaseForm.process will accept the object
              for the named form, and eventually it will end up in
              SelectMultipleField.process_data and get assigned to .data
            """
            setattr(self, name, choices)

    for beaver_attendance in beaver_attendances:
        if beaver_attendance.present:
            selected.append(beaver_attendance.beaver_id)

    selectedChoices = ChoiceObj('beavers', selected)
    form = BeaverAttendanceForm(obj=selectedChoices)
    form.beavers.choices = []

    for beaver in beavers:
        name = beaver.first_name + " " + beaver.surname
        choice = (beaver.id, name)
        form.beavers.choices.append(choice)

    if form.validate_on_submit():
        present = form.beavers.data
        for beaver in beavers:
            beaver_attendance_list = BeaverAttendance.query.filter_by(beaver_id=beaver.id, attendance_id=attendance_id).all()
            try:
                beaver_attendance = beaver_attendance_list[0]
            except:
                beaver_attendance = None
            if beaver.id in present:
                if beaver_attendance is None:
                    beaver_attendance = BeaverAttendance(attendance_id,
                                                         beaver.id,
                                                         True)
                    db.session.add(beaver_attendance)
                else:
                    beaver_attendance.present = True

            elif beaver.id not in present:
                    if beaver_attendance is None:
                        beaver_attendance = BeaverAttendance(attendance_id,
                                                             beaver.id,
                                                             False)
                        db.session.add(beaver_attendance)
                    else:
                        beaver_attendance.present = False
            db.session.commit()
    return render_template("register.html", beavers=beavers, form=form)


class BeaverModelView(ModelView):
    """
    Custom view for Flask-Admin. Adds emergency contacts as inline model and
    modifies update behaviour
    """
    inline_models = (EmergencyContact,)  # comma needed for some reason

    def on_model_change(self, form, model, is_created):
        """When a Beaver record is created or modified ensures that it has
        a BeaverBadge record for all Badges and that the BeaverBadge has the
        correct criteria
        """
        badges = db.session.query(Badge).all()
        beaver_badges = []
        for badge in model.badges:
            beaver_badges.append(badge.badge_id)
        for badge in badges:
            if badge.id not in beaver_badges:
                beaver_badge = BeaverBadge(model.id, badge.id, False)
                db.session.add(beaver_badge)
                db.session.commit()
                app.logger.info("Created Badge")

                for criterion in badge.criteria:
                    badge_id = badge.id
                    badge_criterion = BadgeCriterion(criterion.id, badge_id,
                                                     False)
                    db.session.add(badge_criterion)
                    db.session.commit()
                    app.logger.info("Criterion Created")
            else:
                app.logger.info("Badge not created")


class BadgeModelView(ModelView):
    """
    Custom view for Flask-Admin. Adds criterion as inline model and
    modifies update behaviour
    """
    inline_models = (Criterion,)

    def on_model_change(self, form, model, is_created):
        """When a Badge record is created or modified ensures that it has
        a BeaverBadge record for all Beavers and that the BeaverBadge has the
        correct criteria
        """
        beavers = db.session.query(Beaver).all()
        for beaver in beavers:
            beaver_badges = []
            for badge in beaver.badges:
                beaver_badges.append(badge.badge_id)
            if model.id not in beaver_badges:
                beaver_badge = BeaverBadge(beaver.id, model.id, False)
                db.session.add(beaver_badge)
                db.session.commit()
                app.logger.info("Created Badge")

                for criterion in model.criteria:
                    badge_id = beaver_badge.id  # badge[0].id
                    badge_criterion = BadgeCriterion(criterion.id, badge_id,
                                                     False)
                    db.session.add(badge_criterion)
                    db.session.commit()
                    app.logger.info("Criterion Created")
            else:
                app.logger.info("Badge not created")
                for beaver_badge in beaver.badges:
                    if beaver_badge.badge_id == model.id:
                        criteria = []
                        for badge_criterion in beaver_badge.criteria:
                            criteria.append(badge_criterion.criterion_id)
                        for criterion in model.criteria:
                            if criterion.id not in criteria:
                                badge_id = beaver_badge.id  # badge[0].id
                                badge_criterion = BadgeCriterion(criterion.id,
                                                                 badge_id,
                                                                 False)
                                db.session.add(badge_criterion)
                                db.session.commit()
                                app.logger.info("Criterion Created")


class TripModelView(ModelView):
    """
    Custom view for Flask-Admin modifying update behaviour
    """
    def on_model_change(self, form, model, is_created):
        """When a Trip record is created or modified ensures that it has
        a BeaverTrip record for all Beavers.
        """
        beavers = db.session.query(Beaver).all()
        for beaver in beavers:
            beaver_trips = []
            for trip in beaver.trips:
                beaver_trips.append(trip.trip_id)
            if model.id not in beaver_trips:
                beaver_trip = BeaverTrip(beaver.id, model.id, False, False)
                db.session.add(beaver_trip)
                db.session.commit()
                app.logger.info("BeaverTrip Created")
            else:
                app.logger.info("BeaverTrip not created")


class AttendanceModelView(ModelView):
    """
    Custom view for Flask-Admin. Adds BeaverAttendance as an inline view
    """
    inline_models = (BeaverAttendance,)


# Debugging only
class BeaverBadgeModelView(ModelView):
    """
    Only used for debugging. Custom view for Flask-Admin. Adds BadgeCriterion
    as an inline view
    """
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
