"""
This module contains SQLAlchemy model definitions to create SQL tables
"""
from app import db
import sqlalchemy_utils


class EmergencyContact(db.Model):
    """
    Model for an Emergency contact

    Attributes:
        id (int): Unique Primary Key.
        beaver_id (int): Foreign Key for the :class:`Beaver` table
        beaver (Beaver): Provides direct access to the :class:`Beaver` that is
        linked to the contact
        first_name (str): The contact's first name
        surname (str): The contact's surname
        email (str): The contact's email
        phone_number (str): The contact's phone number
        address_line1 (str): The contact's first address line
        address_line2 (str): The contact's first second address line
        town (str): The town in which the Contact lives
        county (str): The county in which the Contact lives
        postcode (str): The contact's postcode

    """
    id = db.Column(db.Integer, primary_key=True)
    beaver_id = db.Column(db.Integer, db.ForeignKey('beaver.id'))
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(256))
    phone_number = db.Column(db.String(11))
    address_line1 = db.Column(db.String(64))
    address_line2 = db.Column(db.String(64))
    town = db.Column(db.String(64))
    county = db.Column(db.String(64))
    postcode = db.Column(db.String(64))

    def __repr__(self):
        """
        Returns a more human readable represantation of `EmergencyContact`
        """
        return '<EmergencyContact %r> for: ' % (self.first_name,
                                                self.beaver_id)


class Beaver(db.Model):
    """
    Model for a beaver

    Attributes:
        id (int): Unique Primary Key.
        first_name (str): The beaver's first name
        surname (str): The beaver's surname
        dob (DateTime): The beaver's date of birth
        lodge_id (int): Foreign key for :class:`Lodge` table
        lodge_id (int): Provides direct access to the :class:`Lodge` that is
                        that is linked to the beaver
        contacts (list[:class:`EmergencyContact`]): A list of
                                                    :class:`EmergencyContact`
                                                    objects associated with the
                                                    beaver
        badges (list[:class:`BeaverBadge`]): A list of :class:`BeaverBadge`
                                             associated with the beaver
        beaver_attendances (list[:class:`BeaverAttendance`]):
                                        A list of :class:`BeaverAttendance`
                                        objects associated with the beaver
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    dob = db.Column(db.DateTime)
    lodge_id = db.Column(db.Integer, db.ForeignKey('lodge.id'))
    contacts = db.relationship('EmergencyContact', backref="beaver",
                               lazy="dynamic")

    def __repr__(self):
        """
        Returns a more human readable represantation of `Beaver`
        """
        return '<Beaver %r>' % (self.first_name + " " + self.surname)


class Lodge(db.Model):
    """
    Model for a Lodge (group of beavers)

    Attributes:
        id (int): Unique Primary Key.
        name (str): Name of the lodge
        beavers (list[:class:`Beaver`]): A list of beavers asscociated with the
                                         lodge
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    beavers = db.relationship('Beaver', backref="lodge", lazy="dynamic")

    def __repr__(self):
        """
        Returns a more human readable represantation of `Lodge`
        """
        return '<Lodge %r>' % self.name


class Badge(db.Model):
    """
    Model for a Badge

    Attributes:
        id (int): Unique Primary Key.
        name (str): Name of the badge
        img_url (str): URL for the badge image
        beavers_badges (list[:class:`BeaverBadge`]): A list of beavers_badges
                                                     asscociated with the lodge
    """
    __tablename__ = "badge"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    img_url = db.Column(db.String(64))
    beaver_badges = db.relationship('BeaverBadge', backref="badge",
                                    lazy="dynamic")

    def __repr__(self):
        """
        Returns a more human readable represantation of `Badge`
        """
        return '<Badge %r>' % self.name


class BeaverBadge(db.Model):
    """
    Model for a BeaverBadge. Acts as an intermediary between :class:`Beaver`
    and :class:`Badge`

    Args:
        beaver_id (int): Foreign key for :class:`Beaver`
        badge_id (int): Foreign key for :class:`Badge`
        completed (bool): Represents whether the badge has been completed or
                          not

    Attributes:
        id (int): Unique Primary Key.
        beaver (:class:`Beaver`): Provides a link to the :class:`Beaver` that
                                  badge is asscociated with
    """
    __tablename__ = "beaverbadge"
    id = db.Column(db.Integer, primary_key=True)
    beaver_id = db.Column(db.Integer, db.ForeignKey('beaver.id'))
    beaver = db.relationship('Beaver', backref="badges")
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'))
    completed = db.Column(db.Boolean)

    def __init__(self, beaver_id, badge_id, completed):
        self.beaver_id = beaver_id
        self.badge_id = badge_id
        self.completed = completed

    def __repr__(self):
        """
        Returns a more human readable represantation of `BeaverBadge`
        """
        return '<BeaverBadge %r> for: %r' % (self.id, self.beaver.first_name)


class Criterion(db.Model):
    """
    Model for a Criterion.

    Attributes:
        id (int): Unique Primary Key.
        badge_id (int): Foreign key for :class:`Badge`
        badge (:class:`Badge`): Provides a link to the :class:`Badge` that
                                  criterion is asscociated with
        description (str): Desription of criterion
    """
    __tablename__ = "criterion"
    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'))
    badge = db.relationship('Badge', backref="criteria")
    description = db.Column(db.String(128))

    def __repr__(self):
        """
        Returns a more human readable represantation of `Criterion`
        """
        return '<Criterion %r> Desc: %r' % (self.id, self.description)


class BadgeCriterion(db.Model):
    """
    Model for a BadgeCriterion. Acts as an intermediary between
    :class:`BeaverBadge` and :class:`Criterion`

    Args:
        criterion_id (int): Foreign key for :class:`Criterion`
        badge_id (int): Foreign key for :class:`BeaverBadge`
        completed (bool): Represents whether the criterion has been completed
                          or not

    Attributes:
        id (int): Unique Primary Key.
        criterion (:class:`Crterion`): Provides a link to the
                                       :class:`Criterion` that criterion is
                                       asscociated with
        badge (:class:`BeaverBadge`): Provides a link to the
                                      :class:`BeaverBadge` that criterion is
                                      asscociated with
        description (str): Desription of criterion
    """
    id = db.Column(db.Integer, primary_key=True)
    criterion_id = db.Column(db.Integer, db.ForeignKey('criterion.id'))
    criterion = db.relationship('Criterion', backref="criteria")
    badge_id = db.Column(db.Integer, db.ForeignKey('beaverbadge.id'))
    badge = db.relationship('BeaverBadge', backref="criteria")
    completed = db.Column(db.Boolean)

    def __init__(self, criterion_id, badge_id, completed):
        self.criterion_id = criterion_id
        self.badge_id = badge_id
        self.completed = completed

    def __repr__(self):
        """
        Returns a more human readable represantation of `BadgeCriterion`
        """
        return '<BadgeCriterion %r> for Badge: %r' % (self.id, self.badge_id)


class Trip(db.Model):
    """
    A model for a Trip.

    Attributes:
        id (int): Unique Primary Key.
        location (str): Place Name
        cost (numeric): Cost of trip [Max Value of 99999.99]
        date (DateTime): Date of trip
        overnight (bool): Whether trip is overight
        number_of_nights (int): Number of nights the trip is
    """
    __tablename__ = "trip"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128))
    cost = db.Column(db.Numeric(7, 2))  # Maximum value of 99999.99
    date = db.Column(db.DateTime)
    overnight = db.Column(db.Boolean)
    number_of_nights = db.Column(db.Integer)

    def __repr__(self):
        """
        Returns a more human readable represantation of `Trip`
        """
        return '<Trip %r> to %r' % (self.id, self.location)


class BeaverTrip(db.Model):
    """
    Model for a BeaverTrip. Acts as intermediary between :class:`Beaver` and
    :class:`Trip`

    Args:
        beaver_id (int): Foreign key for :class:`Beaver`
        trip_id (int): Foreign key for :class:`Trip`
        permission (bool): Represents whether the criterion has been completed
                          or not
        paid (bool): Represents whether the criterion has been completed or not

    Attributes:
        id (int): Unique Primary Key.
        beaver (:class:`Beaver`): Provides a link to the
                                       :class:`Beaver` that BeaverTrip is
                                       asscociated with
        trip (:class:`Trip`): Provides a link to the :class:`Trip` that
                                  BeaverTrip is asscociated with
    """
    id = db.Column(db.Integer, primary_key=True)
    beaver_id = db.Column(db.Integer, db.ForeignKey('beaver.id'))
    beaver = db.relationship('Beaver', backref="trips")
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    trip = db.relationship('Trip', backref="trips")
    permission = db.Column(db.Boolean)
    paid = db.Column(db.Boolean)

    def __init__(self, beaver_id, trip_id, permission, paid):
        self.beaver_id = beaver_id
        self.trip_id = trip_id
        self.permission = permission
        self.paid = paid

    def __repr__(self):
        """
        Returns a more human readable represantation of `BeaverTrip`
        """
        return '<BeaverTrip %r> for: %r' % (self.id, self.beaver_id)


class Attendance(db.Model):
    """
    A model for a meeting. Linked to a :class:`Criterion` to allow automatic
    completetion of badges. If beaver was present for the meeting then the
    criterion is completed.

    Attributes:
        id (int): Unique Primary Key.
        date (DateTime): Date of meeting
        criterion_id (int): Foreign key for :class:`Criterion`
        criterion (:class:`Criterion`): Provides a link to the :class:`Criterion`
                                        that Attendance is asscociated with
    """
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    criterion_id = db.Column(db.Integer, db.ForeignKey('criterion.id'))
    criterion = db.relationship('Criterion', backref="attendances")

    def __repr__(self):
        return '<Attendance %r>' % (self.id)


class BeaverAttendance(db.Model):
    """
    Model for a BeaverAttendance. Acts as an intermediary between
    :class:`Beaver` and :class:`Attendance`

    Args:
        attendance_id (int): Foreign key for :class:`Attendance`
        beaver_id (int): Foreign key for :class:`Beaver`
        present (bool): Represents whether the beaver was been presesnt or not

    Attributes:
        id (int): Unique Primary Key.
        attendance (:class:`Attendance`): Provides a link to the
                                          :class:`Attendance` that
                                          BeaverAttendance is asscociated with

        beaver (:class:`Beaver`): Provides a link to the
                                       :class:`Beaver` that BeaverAttendance is
                                       asscociated with
    """
    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.id'))
    attendance = db.relationship('Attendance', backref="beaver_attendances")
    beaver_id = db.Column(db.Integer, db.ForeignKey('beaver.id'))
    beaver = db.relationship('Beaver', backref="beaver_attendances")
    present = db.Column(db.Boolean)

    def __init__(self, attendance_id, beaver_id, present):
        self.attendance_id = attendance_id
        self.beaver_id = beaver_id
        self.present = present

    def __repr__(self):
        """
        Returns a more human readable represantation of `BeaverAttendance`
        """
        return '<BeaverAttendance %r> for: %r' % (self.id, self.beaver_id)
