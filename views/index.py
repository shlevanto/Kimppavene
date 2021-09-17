from flask import render_template, session, redirect, flash
from db import db

def index_view():
    if session['boat']['id'] == '':
        flash('Sinulla ei ole vielä veneitä järjestelmässä. Luo uusi vene tai liity olemassaolevaan veneeseen avainkoodilla.')
        return redirect('/boats')

    sql = '''SELECT * FROM transactions WHERE boat_id=:session_boat'''
    result = db.session.execute(sql, {'session_boat': session['boat']['id']})
    db.session.commit()

    transactions = result.fetchall()
    return render_template('index.html', transactions=transactions)