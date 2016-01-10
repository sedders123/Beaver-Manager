from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms import widgets


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class BeaverAttendanceForm(Form):
    beavers = MultiCheckboxField("Present: ", coerce=int)


class BeaverSortForm(Form):
    sort_on = SelectField('Sort By', choices=[('surname', 'Surname'),
                          ('first_name', 'First Name'),
                          ('lodge.name', 'Lodge')])
