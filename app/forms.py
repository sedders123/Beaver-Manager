from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class BeaverAttendanceForm(Form):
    beaver_id = IntegerField()
    attendance_id = IntegerField()
    present = BooleanField()
