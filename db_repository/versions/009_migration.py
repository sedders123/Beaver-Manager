from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
attendance = Table('attendance', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('master_attendance_id', Integer),
    Column('beaver_id', Integer),
    Column('present', Boolean),
)

masterattendance = Table('masterattendance', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date', DateTime),
)

mastertrip = Table('mastertrip', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('location', String(length=128)),
    Column('cost', Numeric(precision=7, scale=2)),
    Column('date', DateTime),
    Column('overnight', Boolean),
    Column('number_of_nights', Integer),
)

trip = Table('trip', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('beaver_id', Integer),
    Column('master_trip_id', Integer),
    Column('permission', Boolean),
    Column('paid', Boolean),
)

emergency_contact = Table('emergency_contact', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('beaver_id', Integer),
    Column('first_name', String(length=64)),
    Column('surname', String(length=64)),
    Column('email', String(length=256)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['attendance'].create()
    post_meta.tables['masterattendance'].create()
    post_meta.tables['mastertrip'].create()
    post_meta.tables['trip'].create()
    post_meta.tables['emergency_contact'].columns['email'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['attendance'].drop()
    post_meta.tables['masterattendance'].drop()
    post_meta.tables['mastertrip'].drop()
    post_meta.tables['trip'].drop()
    post_meta.tables['emergency_contact'].columns['email'].drop()
