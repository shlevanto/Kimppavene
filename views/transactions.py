from flask import render_template, request, redirect, session, flash
from datetime import datetime, timedelta
from db import db
from utils import parse_html_datetime, validate_length

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

    # different cost types
    sql = '''SELECT id, type FROM cost_types'''
    result = db.session.execute(sql)
    cost_types = result.fetchall()

    
    return render_template('transactions.html', owners=owners, cost_types=cost_types)


def addusage_view():
    # if users is empty, rerender with error message
    # if both durations are empty, rerender with error message
    users = request.form.getlist('user')
    
    start_datetime = parse_html_datetime(request.form['start_date'])
    end_datetime = parse_html_datetime(request.form['end_date'])
    
    if start_datetime > end_datetime:
        flash('Aloitusajankohta ei voi olla päättymisajankohdan jälkeen.')
        return redirect('/transactions')

    if 'race' in request.form:
        race = request.form['race']
    else:
        race = False

    # timedelta substractions give time in seconds and days so we need to make it hours
    duration = (end_datetime - start_datetime)
    duration_hours = (duration.seconds // 3600) + (duration.days * 24)

    for user in users:
       
        # add row to database with usage, duration / no of users and user
        sql = ''' INSERT INTO transactions (user_id, boat_id, created, usage_id, amount, start_date, end_date, race) 
                    VALUES (:user_id, :boat_id, NOW(), 1, :duration_hours, :start_date, :end_date, :race)
        '''
        db.session.execute(sql, {
            'user_id': user, 'boat_id': session['boat']['id'], 'duration_hours': duration_hours,
            'start_date': start_datetime, 'end_date': end_datetime, 'race': race
        })

        # modify the usage right of the users based on amount of users
        sql = ''' UPDATE owners 
                    SET usage_hours = usage_hours - :usage_hours_per_user 
                    WHERE user_id = :user_id AND boat_id = :boat_id;
                    '''
        db.session.execute(sql, {'usage_hours_per_user': duration_hours / len(users),
            'user_id': user,
            'boat_id': session['boat']['id']
            })

        db.session.commit()
    
    flash('Tapahtuma lisätty.')
    return redirect('/transactions')


def addmaintenance_view():
    # if users is empty, rerender with error message
    # if both durations are empty, rerender with error message
    users = request.form.getlist('user')
    description = request.form['description']
    
    if not validate_length(description, 255):
        flash('Talkootyön kuvaus on liian pitkä.')
        return redirect('/transactions')

    # check the description input

    start_datetime = parse_html_datetime(request.form['start_date'])
    end_datetime = parse_html_datetime(request.form['end_date'])
    
    if start_datetime > end_datetime:
        flash('Aloitusajankohta ei voi olla päättymisajankohdan jälkeen.')
        return redirect('/transactions')
    
    # timedelta substractions give time in seconds and days so we need to make it hours
    duration = (end_datetime - start_datetime)
    duration_hours = (duration.seconds // 3600) + (duration.days * 24)
    
    for user in users:
        sql = ''' INSERT INTO transactions (user_id, boat_id, created, usage_id, amount, start_date, end_date, description) 
                    VALUES (:user_id, :boat_id, NOW(), 2, :duration_hours, :start_date, :end_date, :description)
        '''
        # One hour of maintenance buys 3 hours of usage
        db.session.execute(sql, {
            'user_id': user, 'boat_id': session['boat']['id'], 'duration_hours': duration_hours,
            'start_date': start_datetime, 'end_date': end_datetime,
            'description': description
        })

        # modify the usage right
        sql = ''' UPDATE owners 
                    SET usage_hours = usage_hours + :usage_hours_per_user 
                    WHERE user_id = :user_id AND boat_id = :boat_id;
                    '''
        db.session.execute(sql, {'usage_hours_per_user': duration_hours * 3,
            'user_id': user,
            'boat_id': session['boat']['id']
            })

        db.session.commit()
    
    flash('Talkootyö lisätty.')
    return redirect('/transactions')


def addcost_view():
    amount = request.form['amount']
    cost_type = request.form['cost_type']
    description = request.form['description']

    if float(amount) <= 0:
        flash('Kulun on oltava suurempi kuin 0.')
        return redirect('/transactions')
    

    start_datetime = parse_html_datetime(request.form['start_date'])
    end_datetime = start_datetime
    
    sql = '''INSERT INTO transactions (user_id, boat_id, created, usage_id, amount, start_date, end_date, description, cost_type_id) 
                    VALUES (:user_id, :boat_id, NOW(), 3, :amount, :start_date, :end_date, :description, :cost_type)  '''    
    
    db.session.execute(sql, {
            'user_id': session['user']['id'], 'boat_id': session['boat']['id'], 
            'amount':amount, 'start_date': start_datetime, 'end_date': end_datetime,
            'description': description, 'cost_type': cost_type
        })
    
    db.session.commit() 

    flash('Kulu lisätty.')
    return redirect('/transactions')

