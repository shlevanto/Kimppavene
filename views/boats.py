from secrets import token_hex
from datetime import date
from flask import render_template, request, session, redirect, flash
from db import db
from utils import validate_length, validate_year


def boats_view():
    # 1.1. get owners of current boat and info on whether they are admins for the boat
    if session['boat']['id'] == '':
        current_boat = None
        owners = None
        is_admin = None
    else:
        # get info on current / session boat
        sql = '''SELECT id, name, type, year, description FROM boats WHERE id=:session_boat'''
        result = db.session.execute(sql, {'session_boat': session['boat']['id']})
        db.session.commit()
        current_boat = result.fetchone()

        # get owners and admin status for current / session boat
        sql = '''SELECT first_name, last_name, boat_admin
                    FROM (
                        SELECT users.first_name, users.last_name, owners.boat_admin, owners.boat_id 
                            FROM users 
                        JOIN owners ON users.id = owners.user_id
                        ) AS boat_owners 
                        WHERE boat_owners.boat_id=:session_boat
                '''
        result = db.session.execute(sql, {'session_boat': session['boat']['id']})
        db.session.commit()
        owners = result.fetchall()

        # is the current user an admin of the current boat?
        sql = '''
            SELECT boat_admin 
                FROM owners 
                WHERE (user_id=:session_user AND boat_id=:session_boat)
            '''
        result = db.session.execute(
            sql, {
                'session_user': session['user']['id'],
                'session_boat': session['boat']['id']
                }
            )

        db.session.commit()
        is_admin = result.fetchone()

    # 2. get all boats of a user
    sql = '''
        SELECT boats.name, boats.id 
            FROM boats 
                JOIN owners ON boats.id=owners.boat_id 
                WHERE owners.user_id=:session_user
        '''
    result = db.session.execute(sql, {'session_user': session['user']['id']})
    db.session.commit()
    user_boats = result.fetchall()

    return render_template(
        'boats.html',
        current_boat=current_boat,
        owners=owners,
        is_admin=is_admin,
        user_boats=user_boats
        )


def chooseboat_view():
    boat_id = request.form['boat_id']
    boat_name = request.form['boat_name']

    session['boat'] = {
        'id': boat_id,
        'name': boat_name
        }

    return redirect('/boats')


def addboat_view():
    print(request.form)
    user_id = session['user']['id']
    key = token_hex(3)
    boat_name = request.form['boat_name']
    boat_type = request.form['boat_type']
    boat_year = request.form['boat_year']
    boat_description = request.form['boat_description']

    if not (validate_length(boat_name, 50) and validate_length(boat_type, 50)):
        flash('Veneen nimi tai tyyppi on liian pitkä.')
        return redirect('/boats')


    if not validate_year(boat_year):
        flash('Valmistusvuoden on oltava väliltä 1800 - {}.'.format(date.today().year))
        return redirect('/boats')

    # Inserts new boat, uses the new id to insert ownership
    # a default 12 days = 288 hours of usage is added when creating a boat

    sql = '''
            WITH new_boat_id AS (
                    INSERT INTO boats (name, type, year, description, key)
                    VALUES (:boat_name, :boat_type, :boat_year, :boat_description, :key)
                    RETURNING id
                    )
                INSERT INTO owners (user_id, boat_id, boat_admin, usage_hours)
                VALUES (
                    :user_id, (
                        SELECT id FROM new_boat_id
                        ), TRUE, 288
                    )
            '''
        # there is a small possibility that two keys are identical
        # while this is a narrow possibility, the key value in database is constrained to unique,
        # so we need to make sure the key is not a duplicate

    while True:
        result = db.session.execute('SELECT id FROM boats WHERE key=:key', {'key': key})
        key_is_duplicate = result.fetchall()

        if key_is_duplicate:
            key = token_hex(3)
            continue
        break

    db.session.execute(
        sql, {
            'boat_name': boat_name,
            'boat_type': boat_type,
            'boat_year': boat_year,
            'boat_description': boat_description,
            'key': key,
            'user_id': user_id
            }
        )

    db.session.commit()

    # set new boat as current boat
    result = db.session.execute('SELECT name, id FROM boats WHERE key=:key', {'key': key})
    db.session.commit()

    boat = result.fetchone()

    session['boat'] = {
        'id': boat.id,
        'name': boat.name
        }

    return redirect('/boats')


def joinboat_view():
    key = request.form['boat_key']
    user_id = session['user']['id']

    if not validate_length(key, 6, 6):
        flash('Avaimen pituus on 6 merkkiä.')
        return redirect('/boats')

    # abort if the user is already an owner of the boat

    sql = '''
        SELECT boats.name FROM owners JOIN boats ON owners.boat_id = boats.id WHERE boats.key=:key AND owners.user_id=:user_id
    '''
    result = db.session.execute(sql, {
        'key': key,
        'user_id': user_id
    })

    if result.fetchone():
        boat = result.fetchone()
        flash('Olet jo osakkaana tässä veneessä .')
        return redirect('/boats')
    
    try:
    # a default 12 days = 288 hours of usage is added when creating a boat
        sql = '''
            INSERT INTO owners (boat_id, user_id, usage_hours) 
                VALUES (
                    (SELECT id FROM boats WHERE key=:key), :user_id, 288
                    )
            '''

        db.session.execute(sql, {'key': key, 'user_id': user_id})
        result = db.session.execute('SELECT id, name FROM boats WHERE key=:key', {'key': key})
        db.session.commit()

        boat = result.fetchone()
        session['boat'] = {
            'id': boat.id,
            'name': boat.name
            }
        flash('Liityit veneeseen {}'.format(boat.name))
        return redirect('/boats')

    except:
        flash('Avaimella ei löydy venettä.')
        return redirect('/boats')

    db.session.commit()

    return redirect('/')
