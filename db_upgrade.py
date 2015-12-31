#!flask/bin/python
"""
.. module:: db_upgrade.py
   :synopsis: Upgrades the current database to a newer version containg any changes made to models
   Should run before db_migrate.py


"""
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

print('Current database version: ' + str(v))
