# tests/test_models.py


import datetime
import unittest

from flask.ext.login import current_user

from base import BaseTestCase
from project import bcrypt
from project.models import User


class TestUser(BaseTestCase):

    def test_get_by_id(self):
        # Ensure id is correct for the current/logged in user.
        with self.client:
            self.client.post('/login', data=dict(
                email='test@testing.com', password='testing'
            ), follow_redirects=True)
            self.assertTrue(current_user.id == 1)

    def test_registered_on_defaults_to_datetime(self):
        # Ensure that registered_on is a datetime.
        with self.client:
            self.client.post('/login', data=dict(
                email='test@testing.com', password='testing'
            ), follow_redirects=True)
            user = User.query.filter_by(email='test@testing.com').first()
            self.assertIsInstance(user.registered_on, datetime.datetime)

    def test_check_password(self):
        # Ensure given password is correct after unhashing
        user = User.query.filter_by(email='test@testing.com').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'testing'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

    def test_validate_invalid_password(self):
        # Ensure user can't login when the pasword is incorrect
        with self.client:
            response = self.client.post('/login', data=dict(
                email='test@testing.com', password='wrong_password'
            ), follow_redirects=True)
        self.assertIn('Invalid email and/or password.', response.data)


if __name__ == '__main__':
    unittest.main()
