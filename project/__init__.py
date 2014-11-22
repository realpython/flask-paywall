# project/__init__.py


#################
#### imports ####
#################

import os

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask_mail import Mail
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy


################
#### config ####
################

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

stripe_keys = {
    'stripe_secret_key': app.config['STRIPE_SECRET_KEY'],
    'stripe_publishable_key': app.config['STRIPE_PUBLISHABLE_KEY']
}


login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)

# register our blueprints
from project.main.views import main_blueprint
from project.user.views import user_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)

# flask-login
from models import User

login_manager.login_view = "user.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
