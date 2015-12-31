from app import db
"""
.. module:: models
   :platform: Unix
   :synopsis: Contains SQLAlchemy Modules used to store information about beavers



"""


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line1 = db.Column(db.String(64))
    line2 = db.Column(db.String(64))
    town = db.Column(db.String(64))
    county = db.Column(db.String(64))
    postcode = db.Column(db.String(64))


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(11))


class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beaver_id = db.Column(db.Integer, db.ForeignKey('beaver.id'))
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))


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


class MasterBadge(db.Model):
    __tablename__ = "masterbadge"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    img_url = db.Column(db.String(64))
    criteria = db.relationship('MasterCriterion', backref="master_badge",
                               lazy="dynamic")
    badges = db.relationship('Badge', backref="master_badge", lazy="dynamic")

    def __repr__(self):
        return '<MasterBadge %r>' % self.name


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beaver_id = db.Column(db.Integer, db.ForeignKey('beaver.id'))
    beaver = db.relationship('Beaver', backref="badges")
    master_badge_id = db.Column(db.Integer, db.ForeignKey('masterbadge.id'))
    completed = db.Column(db.Boolean)
    criteria = db.relationship('Criterion', backref="badge", lazy="dynamic")

    def __repr__(self):
        return '<Badge %r> for Beaver: %r' % (self.id, self.beaver_id)


class MasterCriterion(db.Model):
    __tablename__ = "mastercriterion"
    id = db.Column(db.Integer, primary_key=True)
    master_badge_id = db.Column(db.Integer, db.ForeignKey('masterbadge.id'))
    description = db.Column(db.String(128))

    def __repr__(self):
        return '<MasterCriterion %r> Desc: %r' % (self.id, self.description)


class Criterion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    master_badge_id = db.Column(db.Integer, db.ForeignKey('masterbadge.id'))
    master_criterion_id = db.Column(db.Integer, db.ForeignKey('mastercriterion.id'))
    master_criterion = db.relationship('MasterCriterion', backref="criteria")
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'))
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return '<Criterion %r> for Badge: %r' % (self.id, self.badge_id)
