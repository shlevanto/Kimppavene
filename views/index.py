from flask import render_template, session, redirect, flash
from db import db
import pandas as pd

def index_view():
    if session['boat']['id'] == '':
        flash('Sinulla ei ole vielä veneitä järjestelmässä. Luo uusi vene tai liity olemassaolevaan veneeseen avainkoodilla.')
        return redirect('/boats')


    '''
    SELECT * FROM transactions T JOIN users U ON T.user_id = U.id JOIN usage US ON T.usage_id = US.id JOIN boats B ON T.boat_id = B.id JOIN cost_types ON T.id = cost_types.id JOIN income_types ON T.income_type_id = income_types.id;
    '''

    # sums of costs per cost type
    sql = '''SELECT SUM(amount), cost_types.type 
                FROM report_base 
                    JOIN cost_types ON report_base.cost_type_id = cost_types.id 
                    GROUP BY cost_types.id;
    '''
    
    result = db.session.execute(sql, params={'session_boat': session['boat']['id']})
    data = result.fetchall()
    db.session.commit()

    df = pd.DataFrame(data)
    df.columns = data[0].keys()

    print(df)
    labels = df['type']
    label = 'Menot'
    data = df['sum']

    return render_template('index.html', labels=labels, label=label, data=data)