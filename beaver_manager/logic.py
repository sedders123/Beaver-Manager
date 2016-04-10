"""
This module contains any logic that does not belong in any other module
"""

from beaver_manager import app, db
import datetime
from .email import send_email


def update_criterion(attendance):
    """
    Check whether a beaver was present for a given attendance and if so sets
    the corrosponding ``criterion.completed`` to True

    Args:
        attendance (Attendance): The attendance for which criterion need
                                   updating
    """
    for beaver_attendance in attendance.beaver_attendances:
        for badge in beaver_attendance.beaver.badges:
            for criterion in badge.criteria:
                if criterion.criterion_id == attendance.criterion_id:
                    if beaver_attendance.present:
                        criterion.completed = True
                        db.session.commit()
                    else:
                        criterion.completed = False
                        db.session.commit()


def update_beaver_badge(beaver_badge):
    """
    Checks to see if all the criteria are completed for ``beaver_badge`` and
    if so sets ``beaver_badge.completed`` to True

    Args:
        beaver_badge (BeaverBadge): The beaver badge which need
        checking
    """
    completed = 0
    for criterion in beaver_badge.criteria:
        if criterion.completed:
            completed += 1
    if completed == len(beaver_badge.criteria):
        beaver_badge.completed = True
        db.session.commit()
    else:
        beaver_badge.completed = False
        db.session.commit()


def to_percent(value, total):
    """
    Works out the percentage of a value from a total.

    Args:
        value (int): The value to be converted
        total (int): The total to be used in conversion

    Returns:
        (int): Number between 0.0 and 100.0
    """
    return value / total * 100


def email_contacts_trip(beaver):
    """
    Checks that a beaver has paid and given permission to go on a trip
    """
    now = datetime.datetime.now()
    for beaver_trip in beaver.trips:
        delta_datetime = beaver_trip.trip.date - now
        days_to_trip = delta_datetime.days()
        if days_to_trip > 0 and days_to_trip <= 7:
            if beaver_trip.paid is False:
                need_to_pay = True
            if beaver_trip.permission is False:
                needs_permission = True
            if need_to_pay or needs_permission:
                location = beaver_trip.trip.location
                subject = "Beaver Trip to {}".format(location)
                recipients = []
                for contact in beaver.contacts:
                    recepients.append(contact.email)
                date = beaver_trip.trip.date

                if need_to_pay and needs_permission:
                    needed = "permission form and payment"
                elif need_to_pay:
                    needed = "payment"
                elif needs_permission:
                    needed = "permission form"

                text_body = """
                Hi,
                On {} we are going to {}. We are currently waiting for {}'s {}.
                Could you get this to us as soon as possble,
                Thanks,
                Beaver Leader Team
                """
                text_body = text_body.format(date, location,
                                             beaver.first_name, needed)
                html_body = text_body
                send_email(subject, recipients, text_body, html_body)
