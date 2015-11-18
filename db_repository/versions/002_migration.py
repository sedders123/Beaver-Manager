from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
badge = Table('badge', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('beaver_id', Integer),
    Column('master_badge_id', Integer),
    Column('completed', Boolean),
)

beaver = Table('beaver', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=64)),
    Column('surname', String(length=64)),
    Column('dob', DateTime),
)

criterion = Table('criterion', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('master_criterion_id', Integer),
    Column('badge_id', Integer),
    Column('completed', Boolean),
)

lodge = Table('lodge', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
)

master_badge = Table('master_badge', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('img_url', String(length=64)),
)

master_criterion = Table('master_criterion', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('master_badge_id', Integer),
    Column('description', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['badge'].create()
    post_meta.tables['beaver'].create()
    post_meta.tables['criterion'].create()
    post_meta.tables['lodge'].create()
    post_meta.tables['master_badge'].create()
    post_meta.tables['master_criterion'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['badge'].drop()
    post_meta.tables['beaver'].drop()
    post_meta.tables['criterion'].drop()
    post_meta.tables['lodge'].drop()
    post_meta.tables['master_badge'].drop()
    post_meta.tables['master_criterion'].drop()
