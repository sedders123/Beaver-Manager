from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('master_badge_id', INTEGER),
    Column('completed', BOOLEAN),
)

badge = Table('badge', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('img_url', String(length=64)),
)

criterion = Table('criterion', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('master_badge_id', INTEGER),
    Column('description', VARCHAR(length=128)),
)

criterion = Table('criterion', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('badge_id', Integer),
    Column('description', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['badge'].create()
    pre_meta.tables['criterion'].columns['master_badge_id'].drop()
    post_meta.tables['criterion'].columns['badge_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['badge'].drop()
    pre_meta.tables['criterion'].columns['master_badge_id'].create()
    post_meta.tables['criterion'].columns['badge_id'].drop()
