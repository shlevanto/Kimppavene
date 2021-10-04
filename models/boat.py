from flask import session
from db import db


def owners():
    sql = '''
        SELECT first_name, last_name, boat_admin
            FROM (
                SELECT users.first_name, users.last_name, owners.boat_admin, owners.boat_id 
                    FROM users 
                    JOIN owners ON users.id = owners.user_id
                ) AS boat_owners 
            WHERE boat_owners.boat_id=:session_boat
    '''
    
    result = db.session.execute(sql, {'session_boat': session['boat']['id']})
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
    