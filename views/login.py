from secrets import token_hex
from werkzeug.security import check_password_hash
from flask import render_template, request, session, redirect, flash
from db import db
from utils import validate_length
import models.boat

def login_view():
    try:
        current_user = session['user']
        return redirect('/')
    except KeyError:
        return render_template('login.html')


def loginuser_view():
    username = request.form['username']
    password = request.form['password']

    if not (validate_length(username, 30) and validate_length(password, 30)):
        flash('Käyttäjänimi tai salasana liian pitkä.')
        return redirect('/login')

    sql = 'SELECT * FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()

    if not user:
        flash('Virheellinen käyttäjätunnus tai salasana.')
        return redirect('/login')

    hash_value = user.password

    if not check_password_hash(hash_value, password):
        flash('Virheellinen käyttäjätunnus tai salasana.')
        return redirect('/login')

    session['user'] = {
        'username': user.username,
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name
        }
    session['csrf_token'] = token_hex(16)

    boats = models.boat.user_boats()

    if not boats:
        session['boat'] = {
            'id': '',
            'name': ''}
        flash(
            '''
                Sinulla ei ole vielä veneitä järjestelmässä. 
                Luo uusi vene tai liity olemassaolevaan veneeseen avainkoodilla.
            '''
        )

        return redirect('/boats')

    if len(boats) > 1:
        session['boat'] = {
            'id': '',
            'name': ''}

        flash(
            '''
                Sinulla on useita veneitä järjestelmässä. 
                Valitse mitä venettä haluat tarkastella.
            '''
        )

        return redirect('/boats')

    session['boat'] = {
        'id': boats[0].id,
        'name': boats[0].name
    }

    return redirect('/')
