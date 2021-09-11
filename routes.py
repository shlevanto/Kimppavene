from app import app
from db import db
from flask import redirect, render_template, session, request, url_for, flash
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash
from utils import login_required, validate_alphanum, validate_length, validate_year
from secrets import token_hex
from datetime import date

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# template for chart route
@app.route('/chart')
@login_required
def chart():
    labels = ['Tom', 'Dick', 'Harry']
    label = 'No. of things'
    data = [1, 3, 4]
    return render_template('chart.html', labels=labels, label=label, data=data)


@app.route('/login')
def login():
    # if a user is logged in, we redirect to index
    try:
        current_user = session['user']
        return redirect('/')
    except(KeyError):
        return render_template('login.html')


@app.route('/loginuser', methods=['POST'])
def loginuser():
    username = request.form['username']
    password = request.form['password']

    if not (validate_length(username, 30) and validate_length(password, 30)):
        flash('Käyttäjänimi tai salasana liian pitkä.')
        return redirect('/login')


    # get user
    sql = 'SELECT * FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()

    if not user:
        flash('Virheellinen käyttäjätunnus tai salasana.')
        return redirect('/login')
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session['user'] = {
                                'username': user.username, 
                                'id': user.id, 
                                'first_name': user.first_name, 
                                'last_name': user.last_name
                                }
            
            sql = '''SELECT name, id FROM boats  WHERE id = (SELECT boat_id FROM owners WHERE user_id=:user_id LIMIT 1)'''
            result = db.session.execute(sql, {'user_id': user.id})
            # this now selects the first boat of the owner
            # it should check how many boats the user has
            # if 0 --> redirect to create / join boat
            # if > 1 --> redirect to choose boat

            boat = result.fetchone()
            

            if boat is not None:
                session['boat'] = {
                                'id': boat.id,
                                'name': boat.name 
                }
                return redirect('/')
            else: 
                session['boat'] = {'id':'',
                                    'name':''}
                return redirect('/boats')
        else:
            flash('Virheellinen käyttäjätunnus tai salasana.')
            return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/registeruser', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    
    if not validate_length(password, min=8):
        flash('Salasanan on oltava vähintään 8 merkkiä pitkä.')
        return redirect('/register')
    
    if not (validate_length(username, 30) and validate_length(password, 30)):
        flash('Käyttäjätunnus tai salasana on liian pitkä.')
        return redirect('/register')

    else:
        hash_value = generate_password_hash(password)
        sql = '''INSERT INTO users (username, password, first_name, last_name, email)
                 VALUES(:username, :password, :first_name, :last_name, :email)'''
        
        try:
            db.session.execute(sql, {'username': username, 'password': hash_value, 
                                     'first_name': first_name, 'last_name': last_name, 'email': email})
            db.session.commit()
        
        except exc.IntegrityError:
            flash('Käyttäjätunnus {} on jo käytössä.'.format(username))
            return redirect('/register')

        return redirect('/login')

@app.route('/boats')
@login_required
def boats():
    # to-do 
    # 1. show info on current boat

    if session['boat']['id'] == '':
        current_boat = None
    else:
        sql = '''SELECT name, type, year, description FROM boats WHERE id=:session_boat'''
        result = db.session.execute(sql, {'session_boat': session['boat']['id']})
        db.session.commit()
        current_boat = result.fetchone()

    # 1.1. get owners of current boat
    if session['boat']['id'] == '':
        current_boat = None
        owners=None
    else:
        sql = '''SELECT first_name, last_name 
                    FROM users 
                    WHERE id 
                    IN (
                        SELECT user_id FROM owners WHERE boat_id=:session_boat
                        )
'''
        result = db.session.execute(sql, {'session_boat': session['boat']['id']})
        db.session.commit()
        owners = result.fetchall()

    # sql = '''SELECT '''
    # 2. change to another boat
    # 3. delete boat?

    return render_template('boats.html', current_boat=current_boat, owners=owners)


@app.route('/addboat', methods=['POST'])
@login_required
def addboat():
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


@app.route('/joinboat', methods=['POST'])
@login_required
def joinboat():
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

