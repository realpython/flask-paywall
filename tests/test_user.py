# tests/test_user.py


import datetime
import unittest
import stripe

from flask.ext.login import current_user

from base import BaseTestCase
from project import db
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
        # Ensure logout route requires logged in user.
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn('Please log in to access this page', response.data)

    def test_member_route_requires_login(self):
        # Ensure member route requires logged in user.
        response = self.client.get('/members', follow_redirects=True)
        self.assertIn('Please log in to access this page', response.data)

    def test_member_route_requires_payment(self):
        # Ensure member route requires a paid user.
        user = User(email="unpaid@testing.com", password="testing", paid=False)
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="unpaid@testing.com", password="testing"),
                follow_redirects=True
            )
            self.assertIn('Sorry. You must pay to access this page.', response.data)

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

    def test_user_registration_error(self):
        # Ensure registration behaves correctly.
        token = stripe.Token.create(
            card={
                'number': '4242424242424242',
                'exp_month': '06',
                'exp_year': str(datetime.datetime.today().year + 1),
                'cvc': '123',
            }
        )
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(
                    email="new@tester.com",
                    password="testing",
                    confirm="testing",
                    card_number="4242424242424242",
                    cvc="123",
                    expiration_month="01",
                    expiration_year="2015",
                    stripeToken=token.id,
                ),
                follow_redirects=True
            )
            user = User.query.filter_by(email='new@tester.com').first()
            self.assertEqual(user.email, 'new@tester.com')
            self.assertTrue(user.paid)
            self.assertIn('Thanks for paying!', response.data)
            self.assertTrue(current_user.email == "new@tester.com")
            self.assertTrue(current_user.is_active())
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
