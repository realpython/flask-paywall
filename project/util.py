# project/util.py


from functools import wraps

from flask import flash, redirect, url_for
from flask.ext.login import current_user


def check_paid(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.paid is False:
            flash("Sorry. You must pay to access this page.", 'danger')
            return redirect(url_for('user.register'))
        return func(*args, **kwargs)

    return decorated_function
