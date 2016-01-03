from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
phone_number = Table('phone_number', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('phone_number', VARCHAR(length=11)),
)

emergency_contact = Table('emergency_contact', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('beaver_id', Integer),
    Column('first_name', String(length=64)),
    Column('surname', String(length=64)),
    Column('email', String(length=256)),
    Column('address_id', Integer),
    Column('phone_number', String(length=11)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['phone_number'].drop()
    post_meta.tables['emergency_contact'].columns['address_id'].create()
    post_meta.tables['emergency_contact'].columns['phone_number'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['phone_number'].create()
    post_meta.tables['emergency_contact'].columns['address_id'].drop()
    post_meta.tables['emergency_contact'].columns['phone_number'].drop()
