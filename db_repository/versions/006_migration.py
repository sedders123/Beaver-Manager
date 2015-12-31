from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
master_criterion = Table('master_criterion', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('master_badge_id', INTEGER),
    Column('description', VARCHAR(length=128)),
)

mastercriterion = Table('mastercriterion', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('master_badge_id', Integer),
    Column('description', String(length=128)),
)

criterion = Table('criterion', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('master_badge_id', Integer),
    Column('master_criterion_id', Integer),
    Column('badge_id', Integer),
    Column('completed', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['master_criterion'].drop()
    post_meta.tables['mastercriterion'].create()
    post_meta.tables['criterion'].columns['master_badge_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['master_criterion'].create()
    post_meta.tables['mastercriterion'].drop()
    post_meta.tables['criterion'].columns['master_badge_id'].drop()
