from flask import session
from db import db


def set_time_rates(time_rates={}, initialize=True):
    '''Initializes usage rights for new boat'''

    if initialize:
        new_time_rates = {
            16: 1.0,
            17: 1.0,
            18: 1.0,
            19: 1.0,
            20: 1.25,
            21: 1.25,
            22: 1.5,
            23: 1.5,
            24: 1.75,
            25: 1.75,
            26: 2,
            27: 2,
            28: 2,
            29: 2,
            30: 2,
            31: 2,
            32: 1.75,
            33: 1.75,
            34: 1.5,
            35: 1.5,
            36: 1.25,
            37: 1.25,
            38: 1.0,
            39: 1.0,
            40: 1.0,
            41: 1.0,
            42: 1.0,
            43: 1.0,
            44: 1.0,
        }
        
        for i in new_time_rates:
            sql = '''
                INSERT INTO time_rates (week, ratio, boat_id)
                    VALUES (:week, :ratio, :boat_id)
            '''
            db.session.execute(sql, {
                'week': i,
                'ratio': new_time_rates[i],
                'boat_id': session['boat']['id']
            })

            db.session.commit()


    else:
        new_time_rates = time_rates
        print('time_rates modulissa', new_time_rates)

    for i in new_time_rates:
        sql = '''
            UPDATE time_rates SET ratio=:ratio WHERE boat_id=:boat_id AND week=:week
        '''

        db.session.execute(sql, {
            'week': i,
            'ratio': new_time_rates[i],
            'boat_id': session['boat']['id']
        })

        db.session.commit()


def get_time_rates():
    sql = '''
        SELECT week, ratio 
            FROM time_rates
            WHERE boat_id=:session_boat    
    '''

    result = db.session.execute(sql, {
        'session_boat': session['boat']['id']
        })
    db.session.commit()

    return result.fetchall()
