from app import app
from db import db
from flask import redirect, render_template, session, request
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    return render_template('index.html')


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
    
    def validate_password(password):
        return len(password) >= 8

    if not validate_password(password):
        alert_message = 'Salasanan on oltava vähintään 8 merkkiä pitkä'
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

