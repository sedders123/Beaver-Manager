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
from flask_admin import Admin, AdminIndexView, expose
import datetime

from beaver_manager import app, db
from .models import *
from .views import *
from .forms import *
from .logic import *
from .email import *
from .decorators import *


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return redirect(url_for('index'))


admin = Admin(app, name='beavermanager', template_mode='bootstrap3',
              index_view=MyHomeView())


class ChoiceObj(object):
    def __init__(self, name, choices):
        """
        This is needed so that BaseForm.process will accept the object
        for the named form, and eventually it will end up in
        SelectMultipleField.process_data and get assigned to .data
        """
        setattr(self, name, choices)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(success=None, error=None):
    """
    Displays the homepage

    Args:
        success (str): Message to be displayed in toatr success pop up
        error (str): Message to be displayed in toatr error pop up
    """
    attendances = Attendance.query.all()
    beaver_attendances = []
    for attendance in attendances:
        update_criterion(attendance)
        beaver_badges = BeaverBadge.query.all()
        for beaver_badge in beaver_badges:
            update_beaver_badge(beaver_badge)

        for beaver_attendance in attendance.beaver_attendances:
            beaver_attendances.append(beaver_attendance)

    dates = []
    attendance_data = []
    attendance_data_dict = {}
    for beaver_attendance in beaver_attendances:
        date = beaver_attendance.attendance.date.date().strftime('%d %b %Y')
        if date not in dates:
            dates.append(date)
            attendance_data_dict[date] = []
        attendance_data_dict[date].append(beaver_attendance.present)
    sorted_dates = sorted(dates)
    for date in sorted_dates:
        present = 0
        absent = 0
        attendances = attendance_data_dict[date]
        for attendance in attendances:
            if attendance:
                present += 1
            else:
                absent += 1
        total = present + absent
        percent = to_percent(present, total)
        attendance_data.append(percent)
    height = 40

    now = datetime.datetime.now()
    trips = Trip.query.all()
    upcoming_trips = []
    for trip in trips:
        if trip.date > now:  # checks if date is in the future
            upcoming_trips.append(trip)
    attendances = Attendance.query.all()
    upcoming_attendances = []
    for attendance in attendances:
        if attendance.date > now:
            upcoming_attendances.append(attendance)
    test = ""  #: Doc Can be used to print variables during runtime

    if request.method == "POST":
        form = request.form
        success = None
        error = None
        for field in form:
            if field == "subject":
                subject = form[field]
            elif field == "message":
                message = form[field]
            else:
                app.logger.error("{} posted in email form".format(field))
        contacts = EmergencyContact.query.all()
        contacts_emails = []
        for contact in contacts:
            if contact.email is not None:
                app.logger.info(contact)
                contacts_emails.append(contact.email)
        app.logger.info("Subject: {}\nMessage: {}\nReciepents: {}".format(subject, message, contacts_emails))
        email_sent = send_email(subject, "beavermanagerautomated@gmail.com",
                                contacts_emails, message, message)
        if email_sent:
            success = "Email Sent!"
        else:
            error = "Something went wrong"
        return redirect(url_for('index', success=success, error=error))

    return render_template("index.html", html_title='Home', test=test,
                           dates=sorted_dates, attendance_data=attendance_data,
                           height=height, upcoming_trips=upcoming_trips,
                           upcoming_attendances=upcoming_attendances)


@app.route('/beavers')
def beavers():
    """Queries the database for all beavers then displays a list of them"""
    beavers = Beaver.query.all()
    sort_form = BeaverSortForm()
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
    return render_template("registers.html", attendances=attendances,
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

    success = None
    error = None
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
            else:
                error = "Something went wrong"
            db.session.commit()
        if error is None:
            success = "Changes Saved"
    return render_template("register.html", beavers=beavers, form=form,
                           success=success, error=error)


@app.route('/trips/')
def trips():
    """
    Displays a list of all trips linking to an indiviual view showing more data
    """
    trips = Trip.query.all()
    sort_form = TripSortForm()
    return render_template("trips.html", trips=trips, form=sort_form)


@app.route('/trips/<trip_id>', methods=['GET', 'POST'])
def trip(trip_id):
    """
    Displays information about the trip and allows user to select whether or
    a bevaer has paid for the trip and has permission for the trip

    Args:
        trip_id (int): The ID number of the trip record
    """
    trip = Trip.query.filter_by(id=trip_id).all()
    trip = trip[0]
    beaver_trips = BeaverTrip.query.filter_by(trip_id=trip_id).all()
    beavers = Beaver.query.all()
    paid = []
    permission = []

    for beaver_trip in beaver_trips:
        if beaver_trip.paid:
            paid.append(beaver_trip.beaver_id)
        if beaver_trip.permission:
            permission.append(beaver_trip.beaver_id)

    if request.method == "POST":
        permission_beaver_ids = []
        paid_beaver_ids = []
        for field in request.form:
            if field not in["btn"]:
                split_field = field.split("-")
                field = split_field[0]
                beaver_id = split_field[1]
                beaver_trip = BeaverTrip.query.filter_by(trip_id=trip_id, beaver_id=beaver_id).all()
                beaver_trip = beaver_trip[0]
                if field == "permission":
                    permission_beaver_ids.append(beaver_id)
                    if beaver_id in permission:
                        pass  # No action needed
                    else:
                        beaver_trip.permission = True
                elif field == "paid":
                    paid_beaver_ids.append(beaver_id)
                    if beaver_id in paid:
                        pass  # No action needed
                    else:
                        beaver_trip.paid = True
                db.session.commit()
        app.logger.info("{}:{}".format("Permission", permission_beaver_ids))
        app.logger.info("{}:{}".format("Paid", paid_beaver_ids))

        for beaver in beavers:
            if str(beaver.id) not in permission_beaver_ids:
                beaver_trip = BeaverTrip.query.filter_by(trip_id=trip_id,
                                                         beaver_id=beaver.id
                                                         ).all()
                beaver_trip = beaver_trip[0]
                beaver_trip.permission = False

            if str(beaver.id) not in paid_beaver_ids:
                beaver_trip = BeaverTrip.query.filter_by(trip_id=trip_id,
                                                         beaver_id=beaver.id
                                                         ).all()
                beaver_trip = beaver_trip[0]
                beaver_trip.paid = False
            db.session.commit()
        return redirect(url_for('trip', trip_id=trip_id))

    return render_template("trip.html", trip=trip, paid=paid,
                           permission=permission, beaver_trips=beaver_trips)


class BeaverModelView(ModelView):
    """
    Custom view for Flask-Admin. Adds emergency contacts as inline model and
    modifies update behaviour
    """
    inline_models = (EmergencyContact,)  # comma needed for some reason
    form_excluded_columns = ("badges", "beaver_attendances", "trips")

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

    def on_model_delete(self, model):
        """
        When a beaver is deleted delete all :class:`BeaverBadge`s,
        :class:`BeaverTrip`s, :class:`BeaverAttendance`s and
        :class:`EmergencyContact`s  associated with it.
        """
        beaver_badges = model.badges
        for beaver_badge in beaver_badges:
            for badge_criterion in beaver_badge.criteria:
                db.session.delete(badge_criterion)
            db.session.delete(beaver_badge)
        for beaver_trip in model.trips:
            db.session.delete(beaver_trip)
        for beaver_attendance in model.beaver_attendances:
            db.session.delete(beaver_attendance)
        for emergency_contact in model.contacts:
            db.session.delete(emergency_contact)
        db.session.commit()



class BadgeModelView(ModelView):
    """
    Custom view for Flask-Admin. Adds criterion as inline model and
    modifies update behaviour
    """
    inline_models = (Criterion,)
    form_excluded_columns = ("beaver_badges")

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

    def on_model_delete(self, model):
        """
        When a Badge is deleted, delete all :class:`BeaverBadge`s associated
        with it.
        """
        beaver_badges = model.beaver_badges
        for beaver_badge in beaver_badges:
            for badge_criterion in beaver_badge.criteria:
                db.session.delete(badge_criterion)
            db.session.delete(beaver_badge)
        for criterion in models.criteria:
            db.session.delete(criterion)

        db.session.commit()


class TripModelView(ModelView):
    """
    Custom view for Flask-Admin modifying update behaviour
    """
    form_excluded_columns = ("trips")

    def on_model_change(self, form, model, is_created):
        """
        When a Trip record is created or modified ensures that it has
        a BeaverTrip record for all Beavers.
        """
        beavers = db.session.query(Beaver).all()
        for beaver in beavers:
            beaver_trips = []
            for beaver_trip in beaver.trips:
                beaver_trips.append(beaver_trip.trip_id)
            if model.id not in beaver_trips:
                beaver_trip = BeaverTrip(beaver.id, model.id, False, False)
                db.session.add(beaver_trip)
                db.session.commit()
                app.logger.info("BeaverTrip Created")
            else:
                app.logger.info("BeaverTrip not created")

    def on_model_delete(self, model):
        """
        When a Trip is deleted, delete all :class:`BeaverTrip`s associated with
        it.
        """
        beaver_trips = model.trips
        for beaver_trip in beaver_trips:
            db.session.delete(beaver_trip)
        db.session.commit()

class AttendanceModelView(ModelView):
    """
    Custom view for Flask-Admin. Adds BeaverAttendance as an inline view
    """
    form_excluded_columns = ("beaver_attendances")


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
