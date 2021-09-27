from datetime import date
from datetime import datetime
import re
from functools import wraps
from flask import session, redirect, abort


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            current_user = session['user']
            return func(*args, **kwargs)
        except KeyError:
            return redirect('/login')
    return decorated_function


def validate_length(input_string, max_length=500, min_length=1):
    return (len(input_string) >= min_length) and (len(input_string) <= max_length)


def validate_alphanum(input_string):
    return re.match('^[a-zA-Z0-9_]*$', input_string) is not None


def validate_year(input_year, min_year=1800, max_year=date.today().year):
    return (int(input_year) >= min_year) and (int(input_year) <= max_year)


def parse_html_datetime(input_datetime):
    return datetime.strptime(input_datetime, '%Y-%m-%dT%H:%M')


def csrf(csrf_token):
    if session['csrf_token'] != csrf_token:
        abort(403)  
    