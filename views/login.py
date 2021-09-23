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
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session['user'] = {
                'username': user.username,
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name
                }

            sql = '''
                SELECT name, id 
                    FROM boats WHERE id = (
                        SELECT boat_id FROM owners WHERE user_id=:user_id LIMIT 1
                        )
                '''
            result = db.session.execute(sql, {'user_id': user.id})
            # this now selects the first boat of the owner
            # if 0 --> redirect to create / join boat
            # if > 1 --> redirect to choose boat
            # this needs to be rethought...
            boat = result.fetchone()

            if boat:
                session['boat'] = {
                    'id': boat.id,
                    'name': boat.name
                }
                return redirect('/')
            else:
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
        else:
            flash('Virheellinen käyttäjätunnus tai salasana.')
            return redirect('/login')

