from app import db
import sqlalchemy_utils


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line1 = db.Column(db.String(64))
    line2 = db.Column(db.String(64))
    town = db.Column(db.String(64))
    county = db.Column(db.String(64))
    postcode = db.Column(db.String(64))


class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beaver_id = db.Column(db.Integer, db.ForeignKey('beaver.id'))
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(256))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('Address', backref="emergency_contact")
    phone_number = db.Column(db.String(11))

    def __repr__(self):
        return '<EmergencyContact %r> for: ' % (self.first_name,
                                                self.beaver_id)


class Beaver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    dob = db.Column(db.DateTime)
    lodge_id = db.Column(db.Integer, db.ForeignKey('lodge.id'))
    contacts = db.relationship('EmergencyContact', backref="beaver",
                               lazy="dynamic")

    def __repr__(self):
        return '<Beaver %r>' % (self.first_name + " " + self.surname)


class Lodge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    beavers = db.relationship('Beaver', backref="lodge", lazy="dynamic")

    def __repr__(self):
        return '<Lodge %r>' % self.name


class Badge(db.Model):
    __tablename__ = "badge"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    img_url = db.Column(db.String(64))
    beaver_badges = db.relationship('BeaverBadge', backref="badge",
                                    lazy="dynamic")

    def __repr__(self):
        return '<Badge %r>' % self.name


class BeaverBadge(db.Model):
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
        return '<BeaverBadge %r> for: %r' % (self.id, self.beaver_id)


class Criterion(db.Model):
    __tablename__ = "criterion"
    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'))
    badge = db.relationship('Badge', backref="criteria")
    description = db.Column(db.String(128))

    def __repr__(self):
        return '<Criterion %r> Desc: %r' % (self.id, self.description)


class BadgeCriterion(db.Model):
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
        return '<BadgeCriterion %r> for Badge: %r' % (self.id, self.badge_id)


class Trip(db.Model):
    __tablename__ = "trip"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128))
    cost = db.Column(db.Numeric(7, 2))  # Maximum value of 99999.99
    date = db.Column(db.DateTime)
    overnight = db.Column(db.Boolean)
    number_of_nights = db.Column(db.Integer)

    def __repr__(self):
        return '<Trip %r> to %r' % (self.id, self.location)


class BeaverTrip(db.Model):
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
        return '<BeaverTrip %r> for: %r' % (self.id, self.beaver_id)


class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Attendance %r>' % (self.id)


class BeaverAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.id'))
    attendance = db.relationship('Attendance', backref="beaverattendances")
    beaver_id = db.Column(db.Integer, db.ForeignKey('beaver.id'))
    beaver = db.relationship('Beaver', backref="attendances")
    present = db.Column(db.Boolean)

    def __repr__(self):
        return '<BeaverAttendance %r> for: %r' % (self.id, self.beaver_id)
