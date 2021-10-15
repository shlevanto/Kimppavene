from flask import render_template, redirect, flash, session, request
from db import db
import models.boat
import models.time_rates
from utils import validate_length, validate_year


def manageboat_view():
    if not models.boat.is_admin():
        flash(
            'Sinulla ei ole oikeuksia veneen {} tietojen muokkaamiseen.'
            .format(session['boat']['name'])
            )
        return redirect('/boats')

    current_boat = models.boat.get_boat_info()
    owners = models.boat.owners(exclude=True)
    time_rates = models.time_rates.get_time_rates()

    return render_template('manageboat.html', current_boat=current_boat, owners=owners, time_rates=time_rates)


def editboat_view():
    boat_name = request.form['boat_name']
    boat_type = request.form['boat_type']
    boat_year = request.form['boat_year']
    boat_description = request.form['boat_description']

    if not (validate_length(boat_name, 50) and validate_length(boat_type, 50)):
        flash('Veneen nimi tai tyyppi on liian pitkä.')
        return redirect('/manageboat')

    if not validate_year(boat_year):
        flash('Valmistusvuoden on oltava väliltä 1800 - {}.'.format(date.today().year))
        return redirect('/manageboat')

    if not validate_length(boat_description, 300):
        flash('Veneen kuvaus on liian pitkä.')
        return redirect('/manageboat')

    sql = '''
        UPDATE boats 
            SET name=:boat_name, type=:boat_type, year=:boat_year, description=:boat_description
            WHERE id=:session_boat
    '''

    db.session.execute(sql, {
        'boat_name': boat_name,
        'boat_type': boat_type,
        'boat_year': boat_year,
        'boat_description': boat_description,
        'session_boat': session['boat']['id']
    })

    db.session.commit()

    flash('Veneen tiedot päivitetty.')
    return redirect('/manageboat')


def editboatadmins_view():
    owners = models.boat.owners(exclude=True)
    owner_ids = [owner[2] for owner in owners]
    admin_from_form = [int(user) for user in request.form.getlist('user')]

    allow_admin = set(owner_ids).intersection(set(admin_from_form))

    for user in allow_admin:
        sql = '''
            UPDATE owners SET boat_admin=TRUE WHERE user_id=:user
        '''
        db.session.execute(sql, {'user': user})
        db.session.commit()

    revoke_admin = set(owner_ids).difference(set(admin_from_form))

    for user in revoke_admin:
        sql = '''
            UPDATE owners SET boat_admin=NULL WHERE user_id=:user
        '''
        db.session.execute(sql, {'user': user})
        db.session.commit()

    return redirect('/manageboat')

def edittimerates_view():
    for ratio in request.form.getlist('ratio'):
        if float(ratio) <= 0:
            flash('Kertoimen on oltava suurempi kuin nolla.')
            return redirect('/manageboat')

    time_rates = [float(ratio) for ratio in request.form.getlist('ratio')]
    weeks = list(range(18,40))

    updated_time_rates = dict(zip(weeks, time_rates))

    # update time rates
    models.time_rates.set_time_rates(time_rates=updated_time_rates, initialize=False)
    flash('Käyttöaikakertoimet päivitetty.')

    return redirect('/manageboat')
