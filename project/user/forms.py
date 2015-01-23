# project/users/forms.py


from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from project.models import User


class LoginForm(Form):
    email = TextField(
        'Email Address', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password', validators=[DataRequired()]
    )


class RegisterForm(Form):
    email = TextField(
        'Email Address',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    card_number = TextField(
        'Credit Card Number',
        validators=[DataRequired()]
    )
    cvc = TextField(
        'CVC Code',
        validators=[DataRequired()]
    )
    expiration_month = SelectField(
        'Expiration Month',
        validators=[DataRequired()]
    )
    expiration_year = SelectField(
        'Expiration Year', validators=[DataRequired()]
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
