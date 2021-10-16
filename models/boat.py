from flask import session
from db import db


def owners(exclude=False):
    print(exclude)
    if exclude:
        sql = '''
        SELECT first_name, last_name, id, boat_admin
                FROM (
                    SELECT users.first_name, users.last_name, users.id, owners.boat_admin, owners.boat_id 
                        FROM users 
                        JOIN owners ON users.id = owners.user_id
                    ) AS boat_owners 
                WHERE boat_owners.boat_id=:session_boat 
                    AND NOT (id=:session_user)
        '''

    else:
        sql = '''
            SELECT first_name, last_name, id, boat_admin
                FROM (
                    SELECT users.first_name, users.last_name, users.id, owners.boat_admin, owners.boat_id 
                        FROM users 
                        JOIN owners ON users.id = owners.user_id
                    ) AS boat_owners 
                WHERE boat_owners.boat_id=:session_boat
        '''

    result = db.session.execute(sql, {
        'session_user': session['user']['id'],
        'session_boat': session['boat']['id']
    })
    db.session.commit()

    return result.fetchall()


def user_boats():
    sql = '''
        SELECT boats.name, boats.id 
            FROM boats 
                JOIN owners ON boats.id=owners.boat_id 
                WHERE owners.user_id=:session_user
    '''

    result = db.session.execute(sql, {'session_user': session['user']['id']})
    db.session.commit()

    return result.fetchall()


def is_admin():
    sql = '''
        SELECT boat_admin 
            FROM owners 
            WHERE boat_id=:session_boat AND user_id=:session_user;
    '''

    result = db.session.execute(sql, {
        'session_boat': session['boat']['id'],
        'session_user': session['user']['id']
    })
    db.session.commit()

    return result.fetchone()[0]


def get_boat_info():
    sql = '''
        SELECT id, name, type, year, description, key 
            FROM boats 
            WHERE id=:session_boat'''

    result = db.session.execute(sql, {'session_boat': session['boat']['id']})
    db.session.commit()

    return result.fetchone()


def get_years():
    sql = '''
        SELECT DISTINCT(
            EXTRACT(YEAR FROM start_date)::INT
            ) AS year
            FROM report_base 
            WHERE boat_id=:session_boat
            ORDER BY year DESC
    '''

    result = db.session.execute(sql, {'session_boat': session['boat']['id']})
    years_tuples = result.fetchall()
    db.session.commit()

    if years_tuples == []:
        return False

    else:
        years = []

        for year in years_tuples:
            if year[0]:
                years.append(year[0])
            else:
                return False
    
    return years

