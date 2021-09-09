from functools import wraps
from flask import session, redirect
from datetime import date
import re


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            current_user = session['user']
            return f(*args, **kwargs)
        except(KeyError):
            return redirect('/login')
    return decorated_function


def validate_length(input, max=500, min=1):
    return (len(input) >= min) and (len(input) <= max)


def validate_alphanum(input):
    return re.match('^[a-zA-Z0-9_]*$', input) is not None


def validate_year(input, min=1800, max=date.today().year):
    return (int(input) >= min) and (int(input) <= max)