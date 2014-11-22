# project/util.py


from functools import wraps

from flask import current_app, flash, redirect, url_for
from flask.ext.testing import TestCase
from flask.ext.login import current_user

from project import app, db
from project.models import User


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        user = User(email="ad@min.com", password="admin_user", paid=False)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


def check_paid(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.paid is False:
            flash("Sorry. You must pay to access this page.", 'danger')
            return redirect(url_for('user.members'))
        return func(*args, **kwargs)

    return decorated_function
