from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class NewBeaverForm(Form):
    first_name = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])
    dob = DateField('Date of Birth', format='%m/%d/%Y',
                    validators=[DataRequired()])
