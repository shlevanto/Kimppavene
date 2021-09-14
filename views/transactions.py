from flask import render_template, request, redirect, session
from datetime import datetime, timedelta
from db import db
from utils import parse_html_datetime

def transactions_view():
    # session user is used by default, include other owners of boat too
    sql = '''SELECT first_name, last_name, id 
                    FROM (
                        SELECT users.first_name, users.last_name, users.id, owners.boat_admin, owners.boat_id 
                            FROM users 
                        JOIN owners ON users.id = owners.user_id
                        ) AS boat_owners 
                        WHERE boat_owners.boat_id=:session_boat AND NOT (id=:session_user);
                '''
    result = db.session.execute(sql, {'session_boat': session['boat']['id'], 'session_user': session['user']['id']})
    db.session.commit()
    owners = result.fetchall()
    
    return render_template('transactions.html', owners=owners)


def addusage_view():
    # if users is empty, rerender with error message
    # if both durations are empty, rerender with error message
    users = request.form.getlist('user')
    n_users = len(users)
    
    # handling datetimes is a bit tricky
    start_datetime = parse_html_datetime(request.form['start_date'])
    end_datetime = parse_html_datetime(request.form['end_date'])
    
    if 'competition' in request.form:
        competition = request.form['competition']
    else:
        competition = False

    # why does timedelta give days and seconds... that's just weird
    duration = (end_datetime - start_datetime)
    duration_hours = (duration.seconds // 3600) + (duration.days * 24)

    for user in users:
        # add row to database with usage, duration / no of users and user
        pass


    return str(n_users)
