"""
This module contains any logic that does not belong in any other module
"""

from beaver_manager import app, db


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


def generate_toast(toast_type, message, title):
    """
    Generates a javscript command to be used with the toastr library to
    display a message along the bottom of the screen

    Args:
        toast_type (str): Must be one of `info,warning,success,error`. Decides
                          formatting of popup
        message (str): Message to be displayed in the string
        title (str): Title for popup
    """
    if toast_type not in ["info", "warning", "success", "error"]:
        return ""
    else:
        toast = "'{}','{}'".format(message, title)
        return toast
