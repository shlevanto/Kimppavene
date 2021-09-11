from flask import redirect, render_template, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from sqlalchemy import exc
from utils import validate_length

def register_view():
    return render_template('register.html')

def registeruser_view():
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
