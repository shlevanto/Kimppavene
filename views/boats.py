from flask import render_template, request, session, redirect, flash
from secrets import token_hex
from db import db
from datetime import date
from utils import validate_length


def boats_view():
    # to-do 
    # 1. show info on current boat

    if session['boat']['id'] == '':
        current_boat = None
    else:
        sql = '''SELECT name, type, year, description FROM boats WHERE id=:session_boat'''
        result = db.session.execute(sql, {'session_boat': session['boat']['id']})
        db.session.commit()
        current_boat = result.fetchone()

    # 1.1. get owners of current boat and info on whether they are admins for the boat
    if session['boat']['id'] == '':
        current_boat = None
        owners=None
    else:
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

    

    # for showing who is administrator, something like this is needed
    # SELECT first_name, boat_admin FROM (SELECT users.first_name, owners.boat_admin, owners.boat_id FROM users JOIN owners ON users.id = owners.user_id) AS foo WHERE foo.boat_id = 10;

    # 2. change to another boat
    # 3. delete boat?

    return render_template('boats.html', current_boat=current_boat, owners=owners)


def addboat_view():
    user_id = session['user']['id']
    key = token_hex(3)
    boat_name = request.form['boat_name']
    boat_type = request.form['boat_type']
    boat_year = request.form['boat_year']
    boat_description = request.form['boat_description']

    if not (validate_length(boat_name, 50) and validate_length(boat_type, 50)):
        flash('Veneen nimi tai tyyppi on liian pitkä.')
        return redirect('/boats')


    if not (validate_year(boat_year)):
        flash('Valmistusvuoden on oltava väliltä 1800 - {}.'.format(date.today().year))
        return redirect('/boats')
        # Inserts new boat, uses the new id to insert ownership
    sql = '''
            WITH new_boat_id AS (
                    INSERT INTO boats (name, type, year, description, key)
                    VALUES (:boat_name, :boat_type, :boat_year, :boat_description, :key)
                    RETURNING id
                    )
                INSERT INTO owners (user_id, boat_id, boat_admin)
                VALUES (
                    :user_id, (
                        SELECT id FROM new_boat_id
                        ), TRUE
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

    db.session.execute(sql, {
                                'boat_name': boat_name, 
                                'boat_type': boat_type, 
                                'boat_year': boat_year,
                                'boat_description': boat_description,
                                'key': key,
                                'user_id': user_id
                                })
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

    if not(validate_length(key, 30)):
        flash('Avaimella ei löydy venettä.')
        return redirect('/boats')

    # add a try except here
    sql = '''INSERT INTO owners (boat_id, user_id) VALUES ((SELECT id FROM boats WHERE key=:key), :user_id)'''

    try: 
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
