import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG=True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess-not-so-hidden'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')