import pandas as pd
from flask import render_template, session, redirect, flash
from db import db


def index_view():
    if session['boat']['id'] == '':
        flash(
            '''
                Sinulla ei ole vielä veneitä järjestelmässä. 
                Luo uusi vene tai liity olemassaolevaan veneeseen avainkoodilla.
            '''
            )
        return redirect('/boats')


    # sums of costs per cost type
    sql = '''
        SELECT SUM(amount), cost_types.type
            FROM report_base 
            JOIN cost_types ON report_base.cost_type_id = cost_types.id 
            GROUP BY cost_types.id;
    '''

    result = db.session.execute(sql, params={'session_boat': session['boat']['id']})
    data = result.fetchall()
    db.session.commit()

    data_frame = pd.DataFrame(data)
    data_frame.columns = data[0].keys()

    labels = data_frame['type']
    label = 'Menot'
    data = data_frame['sum']

    return render_template('index.html', labels=labels, label=label, data=data)
