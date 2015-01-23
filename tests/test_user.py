# tests/test_user.py


import datetime
import unittest

from flask.ext.login import current_user

from base import BaseTestCase
from project import bcrypt
from project.models import User
from project.user.forms import LoginForm


class TestUserBlueprint(BaseTestCase):

    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials.
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="test@testing.com", password="testing"),
                follow_redirects=True
            )
            self.assertIn('Welcome', response.data)
            self.assertIn('Logout', response.data)
            self.assertIn('Members', response.data)
            self.assertTrue(current_user.email == "test@testing.com")
            self.assertTrue(current_user.is_active())
            self.assertEqual(response.status_code, 200)

    def test_logout_behaves_correctly(self):
        # Ensure logout behaves correctly - regarding the session.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@testing.com", password="testing"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn('You are logged out. Bye!\n', response.data)
            self.assertFalse(current_user.is_active())

    def test_logout_route_requires_login(self):
        # Ensure logout route requres logged in user.
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn('Please log in to access this page', response.data)

    def test_member_route_requires_login(self):
        # Ensure member route requres logged in user.
        response = self.client.get('/members', follow_redirects=True)
        self.assertIn('Please log in to access this page', response.data)

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(email='test@testing.com', password='admin_user')
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())

    def test_register_route(self):
        # Ensure about route behaves correctly.
        response = self.client.get('/register', follow_redirects=True)
        self.assertIn('<h1>Please Register</h1>\n', response.data)

    # def test_user_registration(self):
    #     # Ensure registration behaves correctlys.
    #     with self.client:
    #         response = self.client.post(
    #             '/register',
    #             data=dict(email="test@tester.com", password="testing",
    #                       confirm="testing"),
    #             follow_redirects=True
    #         )
    #         self.assertIn('Welcome', response.data)
    #         self.assertTrue(current_user.email == "test@tester.com")
    #         self.assertTrue(current_user.is_active())
    #         self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
