from flask import redirect, session


def logout_view():
    session.clear()
    return redirect('/login')
