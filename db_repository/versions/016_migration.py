from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
phonenumber = Table('phonenumber', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('phone_number', VARCHAR(length=11)),
)

emergency_contact = Table('emergency_contact', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('beaver_id', INTEGER),
    Column('first_name', VARCHAR(length=64)),
    Column('surname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=256)),
    Column('address_line1', VARCHAR(length=64)),
    Column('address_line2', VARCHAR(length=64)),
    Column('county', VARCHAR(length=64)),
    Column('postcode', VARCHAR(length=64)),
    Column('town', VARCHAR(length=64)),
    Column('phone_number_id', INTEGER),
)

emergency_contact = Table('emergency_contact', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('beaver_id', Integer),
    Column('first_name', String(length=64)),
    Column('surname', String(length=64)),
    Column('email', String(length=256)),
    Column('phone_number', String(length=11)),
    Column('address_line1', String(length=64)),
    Column('address_line2', String(length=64)),
    Column('town', String(length=64)),
    Column('county', String(length=64)),
    Column('postcode', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['phonenumber'].drop()
    pre_meta.tables['emergency_contact'].columns['phone_number_id'].drop()
    post_meta.tables['emergency_contact'].columns['phone_number'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['phonenumber'].create()
    pre_meta.tables['emergency_contact'].columns['phone_number_id'].create()
    post_meta.tables['emergency_contact'].columns['phone_number'].drop()
