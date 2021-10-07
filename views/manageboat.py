from flask import render_template, redirect, flash, session, request
from db import db
import models.boat
from utils import validate_length, validate_year


def manageboat_view():
    # check that user is this boats admin
    if not models.boat.is_admin():
        return redirect('boats/')

    # get boat info
    current_boat = models.boat.get_boat_info()

    # get boat users
    owners = models.boat.owners()

    # get boat usage rights

    return render_template('manageboat.html', current_boat=current_boat)


def editboat_view():
    # get inputs from form
    boat_name = request.form['boat_name']
    boat_type = request.form['boat_type']
    boat_year = request.form['boat_year']
    boat_description = request.form['boat_description']
    
    # validate inputs
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