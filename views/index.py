import pandas as pd
from flask import render_template, session, redirect, flash, request
from db import db
import models.boat


def index_view(): 
    if session['boat']['id'] == '':
        flash(
            '''
                Sinulla ei ole vielä veneitä järjestelmässä. 
                Luo uusi vene tai liity olemassaolevaan veneeseen avainkoodilla.
            '''
            )
        return redirect('/boats')

    years = models.boat.get_years()

    if not years:
        return render_template('index_empty.html')

    if 'year' in request.args:
        report_year = request.args['year']
    else:
        report_year = years[0]
    
    # Chart 1 usage and maintenance work 
    sql = '''
        SELECT CONCAT(first_name, ' ', last_name) AS name, usage_type, usage_id, SUM(amount) 
            FROM report_base 
            WHERE usage_id IN (1,2)
                AND boat_id=:session_boat
                AND EXTRACT(YEAR FROM start_date)=:report_year
            GROUP BY usage_type, usage_id, name 
            ORDER BY name;
    '''
    result = db.session.execute(sql, {
        'session_boat': session['boat']['id'], 
        'report_year': report_year})
    data = result.fetchall()
    db.session.commit()

    data_frame = pd.DataFrame(data)

    label_usage = 'Käyttö ja talkoot per osakas'
    labels_usage = []
    data_usage_sailing = []
    data_usage_maintenance = []

    if len(data_frame.index) != 0:
        data_frame.columns = data[0].keys()
        labels_usage = pd.unique(data_frame['name'])
        data_usage_sailing = data_frame[data_frame['usage_id']==1]['sum']
        data_usage_maintenance = data_frame[data_frame['usage_id']==2]['sum']

    # Chart 2 usage right left
    sql = '''
        SELECT CONCAT(users.first_name, ' ', users.last_name) AS name, usage_hours 
        FROM owners 
        JOIN users ON owners.user_id=users.id 
            WHERE boat_id=:session_boat;
    '''
    result = db.session.execute(sql, {
        'session_boat': session['boat']['id'],
        'report_year': report_year})
    data = result.fetchall()
    db.session.commit()

    data_frame = pd.DataFrame(data)

    label_usage_right = 'Käyttöoikeutta jäljellä'
    labels_usage_right = []
    data_usage_right = []

    if len(data_frame.index) != 0:
        data_frame.columns = data[0].keys()
        labels_usage_right = data_frame['name']
        data_usage_right = data_frame['usage_hours']

    # Chart 3 sums of costs per cost type
    sql = '''
        SELECT SUM(amount), cost_types.type
            FROM report_base 
            JOIN cost_types ON report_base.cost_type_id=cost_types.id 
            WHERE boat_id=:session_boat AND EXTRACT(YEAR FROM start_date)=:report_year
            GROUP BY cost_types.id;
    '''

    result = db.session.execute(sql, {'session_boat': session['boat']['id'], 'report_year': report_year})
    data = result.fetchall()
    db.session.commit()

    data_frame = pd.DataFrame(data)

    label_cost = 'Kulut per kategoria'
    labels_cost = []
    data_cost = []
    
    if len(data_frame.index) != 0:
        data_frame.columns = data[0].keys()
        labels_cost = data_frame['type']
        data_cost = data_frame['sum']

    # Chart 4 costs by user and cost type
    sql = '''
        SELECT CONCAT(first_name, ' ', last_name) AS name, SUM(amount) 
            FROM report_base 
            JOIN cost_types ON report_base.cost_type_id = cost_types.id 
            WHERE boat_id = :session_boat AND usage_id=3 AND EXTRACT(YEAR FROM start_date) = :report_year 
            GROUP BY name;
    '''
    result = db.session.execute(sql, {'session_boat': session['boat']['id'], 'report_year': report_year})
    data = result.fetchall()
    db.session.commit()

    data_frame_2 = pd.DataFrame(data)

    label_cost_owner = 'Kulut per osakas'
    labels_cost_owner = []
    data_cost_owner = []

    if len(data_frame_2.index) != 0:
        data_frame_2.columns = data[0].keys()
        labels_cost_owner = data_frame_2['name']
        data_cost_owner = data_frame_2['sum']

    
    return render_template(
        'index.html',
        years=years,
        labels_usage=labels_usage, label_usage=label_usage, data_usage_sailing=data_usage_sailing, data_usage_maintenance=data_usage_maintenance,
        label_usage_right=label_usage_right, labels_usage_right=labels_usage_right, data_usage_right=data_usage_right,
        labels_cost=labels_cost, label_cost=label_cost, data_cost=data_cost,
        labels_cost_owner=labels_cost_owner, label_cost_owner=label_cost_owner, data_cost_owner=data_cost_owner
        )
