# tests/test_functional.py


import unittest

from flask.ext.login import current_user

from base import BaseTestCase
from project import db
from project.models import User


class TestPublic(BaseTestCase):

    def test_index(self):
        # Ensure Flask is setup.
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_members_route_requires_login(self):
        # Ensure main route requres logged in user.
        response = self.client.get('/members', follow_redirects=True)
        self.assertIn('Please log in to access this page', response.data)

    def test_logout_route_requires_login(self):
        # Ensure logout route requres logged in user.
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)


class TestLoggingInOut(BaseTestCase):

    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="ad@min.com", password="admin_user"),
                follow_redirects=True
            )
            self.assertIn(b'Welcome', response.data)
            self.assertTrue(current_user.email == "ad@min.com")
            self.assertTrue(current_user.is_active())
            self.assertTrue(response.status_code == 200)

    def test_logout_behaves_correctly(self):
        # Ensure logout behaves correctly, regarding the session
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="ad@min.com", password="admin_user"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You are logged out. Bye!', response.data)
            self.assertFalse(current_user.is_active())


if __name__ == '__main__':
    unittest.main()
