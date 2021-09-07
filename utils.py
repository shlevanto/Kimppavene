from functools import wraps
from flask import session, redirect


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            current_user = session['user']
            return f(*args, **kwargs)
        except(KeyError):
            return redirect('/login')
    return decorated_function