# project/users/forms.py


from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from project.models import User


class LoginForm(Form):
    email = TextField('Email Address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])


class RegisterForm(Form):
    email = TextField(
        'Email Address',
        [DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'Password',
        [DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        [DataRequired(), EqualTo('password', message='Passwords must match.')]
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class StripeForm(Form):
    card_number = TextField('Credit Card Number',)
    cvc = TextField('CVC Code',)
    expiration_month = TextField('Expiration Month',)
    expiration_year = TextField('Expiration Year')
