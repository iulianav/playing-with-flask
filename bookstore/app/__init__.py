from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')

# # Load the configuration from the instance folder
# app.config.from_pyfile('config.py')
#
# # Load the file specified by the APP_CONFIG_FILE environment variable
# # Variables defined here will override those in the default configuration
# app.config.from_envvar('APP_CONFIG_FILE')

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models
api.add_resource(views.SearchResults, '/search')
