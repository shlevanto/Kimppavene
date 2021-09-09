from app import app
from db import db
from flask import redirect, render_template, session, request
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
    alert_message = 'Virheellinen käyttäjänimi tai salasana'

    if not (validate_length(username, 30) and validate_length(password, 30)):
        alert_message = 'Käyttäjänimi tai salasana liian pitkä.'
        return render_template('login.html', alert_message=alert_message)


    # get user
    sql = 'SELECT * FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()

    if not user:
        return render_template('login.html', alert_message=alert_message)
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

            session['boat'] = {
                                'id': boat.id,
                                'name': boat.name 
            }
            return redirect('/')
        else:
            return render_template('login.html', alert_message=alert_message)


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
        alert_message = 'Salasanan on oltava vähintään 8 merkkiä pitkä'
        return render_template('register.html', alert_message=alert_message)
    
    if not (validate_length(username, 30) and validate_length(password, 30)):
        alert_message = 'Käyttäjätunnus tai salasana on liian pitkä.'
        return render_template('register.html', alert_message=alert_message)
    
    else:
        hash_value = generate_password_hash(password)
        sql = '''INSERT INTO users (username, password, first_name, last_name, email)
                 VALUES(:username, :password, :first_name, :last_name, :email)'''
        
        try:
            db.session.execute(sql, {'username': username, 'password': hash_value, 
                                     'first_name': first_name, 'last_name': last_name, 'email': email})
            db.session.commit()
        
        except exc.IntegrityError:
            alert_message = 'Käyttäjätunnus {} on jo käytössä.'.format(username)
            return render_template('register.html', alert_message=alert_message)

        return redirect('/login')

@app.route('/boats')
@login_required
def boats():
    # to-do 
    # 1. show info on current boat
    # 2. change to another boat
    # 3. delete boat?

    return render_template('boats.html')


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
        alert_message = 'Veneen nimi tai tyyppi on liian pitkä'
        return render_template('boats.html', alert_message=alert_message)


    if not (validate_year(boat_year)):
        alert_message = 'Valmistusvuoden on oltava väliltä 1800 - {}'.format(date.today().year)
        return render_template('boats.html', alert_message=alert_message)
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

    return redirect('/')


@app.route('/joinboat', methods=['POST'])
@login_required
def joinboat():
    key = request.form['boat_key']
    user_id = session['user']['id']

    if not(validate_length(key, 30)):
        alert_message = 'Avaimella ei löydy venettä.'
        return render_template('boats.html', alert_message=alert_message)

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
        return render_template('boats.html', success_message='Liityit veneeseen ' + boat.name)
    
    except:
        alert_message = 'Avaimella ei löydy venettä'
        return render_template('boats.html', alert_message=alert_message)

    db.session.commit()

    return redirect('/')

