from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
trip = Table('trip', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('location', String(length=128)),
    Column('cost', String(length=7)),
    Column('date', DateTime),
    Column('overnight', Boolean),
    Column('number_of_nights', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['trip'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['trip'].drop()
