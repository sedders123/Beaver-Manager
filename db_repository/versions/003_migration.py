from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
address = Table('address', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('line1', String(length=64)),
    Column('line2', String(length=64)),
    Column('town', String(length=64)),
    Column('county', String(length=64)),
    Column('postcode', String(length=64)),
)

emergency_contact = Table('emergency_contact', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('beaver_id', Integer),
    Column('first_name', String(length=64)),
    Column('surname', String(length=64)),
)

phone_number = Table('phone_number', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('phone_number', String(length=11)),
)

beaver = Table('beaver', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=64)),
    Column('surname', String(length=64)),
    Column('dob', DateTime),
    Column('lodge_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['address'].create()
    post_meta.tables['emergency_contact'].create()
    post_meta.tables['phone_number'].create()
    post_meta.tables['beaver'].columns['lodge_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['address'].drop()
    post_meta.tables['emergency_contact'].drop()
    post_meta.tables['phone_number'].drop()
    post_meta.tables['beaver'].columns['lodge_id'].drop()
