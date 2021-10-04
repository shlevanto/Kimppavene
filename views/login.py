from secrets import token_hex
from werkzeug.security import check_password_hash
from flask import render_template, request, session, redirect, flash
from db import db
from utils import validate_length

def login_view():
# if a user is logged in, we redirect to index
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

    # get user
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

    # if the login is successfull, set user as session['user']
    session['user'] = {
        'username': user.username,
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name
        }
    session['csrf_token'] = token_hex(16)

    # get list of user's boats
    sql = '''
        SELECT boats.name, boats.id 
            FROM boats 
            JOIN owners ON boats.id=owners.boat_id 
            WHERE owners.user_id=:user_id;
        '''
    result = db.session.execute(sql, {'user_id': user.id})
    boats = result.fetchall()

    # if no boats, redirect to create / join boat
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

    # if many boats, redirect to choose boat
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

    # if one boat, login and redirect to index
    session['boat'] = {
        'id': boats[0].id,
        'name': boats[0].name
    }

    return redirect('/')
