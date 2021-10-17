from flask import render_template, request, redirect, session, flash, make_response
from db import db
from utils import parse_html_datetime, validate_length
import models.boat


def transactions_view():
    if session['boat']['id'] == '':
        flash(
            '''
                Sinulla ei ole vielä veneitä järjestelmässä. 
                Luo uusi vene tai liity olemassaolevaan veneeseen avainkoodilla.
            '''
        )

        return redirect('/boats')

    owners = models.boat.owners(exclude=True)

    sql = '''SELECT id, type FROM cost_types'''
    result = db.session.execute(sql)
    db.session.commit()
    cost_types = result.fetchall()

    sql = '''SELECT id, type FROM income_types'''
    result = db.session.execute(sql)
    db.session.commit()
    income_types = result.fetchall()

    years = models.boat.get_years()

    if not years:
        years = []

    sql = '''SELECT id, usage_type FROM usage GROUP BY id'''
    result = db.session.execute(sql)
    db.session.commit()
    usages = result.fetchall()

    transactions = []

    if request.args:
        usage_type = request.args['usage_type']
        report_year = request.args['year']

        if len(usage_type) > 2 or len(report_year) > 4:
            return redirect('/transactions')

        sql = '''
            SELECT  amount, 
                    EXTRACT(YEAR FROM start_date)::INTEGER AS start_year, 
                    EXTRACT(MONTH FROM start_date)::INTEGER AS start_month,
                    EXTRACT(DAY FROM start_date)::INTEGER AS start_day,
                    EXTRACT(YEAR FROM end_date)::INTEGER AS end_year, 
                    EXTRACT(MONTH FROM end_date)::INTEGER AS end_month,
                    EXTRACT(DAY FROM end_date)::INTEGER AS end_day,
                    description, 
                    cost_type_id, cost_type, 
                    income_type_id, income_type, 
                    CONCAT(first_name, ' ', last_name) as name,
                    attachment_name,
                    transaction_id
                FROM report_base
                    WHERE boat_id=:session_boat
                    AND EXTRACT(YEAR FROM start_date)=:report_year
                    AND usage_id=:usage_type
                ORDER BY start_date
            '''
        result = db.session.execute(sql, {
            'session_boat': session['boat']['id'],
            'report_year': report_year,
            'usage_type': usage_type
            })

        db.session.commit()
        transactions = result.fetchall()


    return render_template(
        'transactions.html',
        owners=owners,
        income_types=income_types,
        cost_types=cost_types,
        usages=usages,
        years=years,
        transactions=transactions
        )


def addusage_view():
    users = request.form.getlist('user')

    start_datetime = parse_html_datetime(request.form['start_date'])
    end_datetime = parse_html_datetime(request.form['end_date'])

    week_no = start_datetime.isocalendar()[1]

    if start_datetime > end_datetime:
        flash('Aloitusajankohta ei voi olla päättymisajankohdan jälkeen.')
        return redirect('/transactions')

    if 'race' in request.form:
        race = request.form['race']
    else:
        race = False

    duration = (end_datetime - start_datetime)
    duration_hours = (duration.seconds // 3600) + (duration.days * 24)

    for user in users:
        sql = '''
            INSERT INTO transactions (
                user_id, boat_id, created, usage_id, amount, start_date, end_date, race
                ) 
                VALUES (
                    :user_id, :boat_id, NOW(), 1, :duration_hours, :start_date, :end_date, :race
                    )
        '''
        db.session.execute(sql, {
            'user_id': user,
            'boat_id': session['boat']['id'],
            'duration_hours': duration_hours,
            'start_date': start_datetime,
            'end_date': end_datetime,
            'race': race
        })

        sql = '''
            UPDATE owners 
                SET usage_hours = usage_hours - (:usage_hours_per_user * 
                    (
                        SELECT COALESCE (
                            (SELECT ratio 
                                FROM time_rates 
                                WHERE boat_id=:boat_id AND week=:week_no), 1.0)))
                WHERE user_id = :user_id AND boat_id = :boat_id;
            '''

        db.session.execute(
            sql, {
                'usage_hours_per_user': duration_hours / len(users),
                'user_id': user,
                'boat_id': session['boat']['id'],
                'week_no': week_no
                }
            )

        db.session.commit()

    flash('Tapahtuma lisätty.')
    return redirect('/transactions')


def addmaintenance_view():
    users = request.form.getlist('user')
    description = request.form['description']

    if not validate_length(description, 255):
        flash('Talkootyön kuvaus on liian pitkä.')
        return redirect('/transactions')

    start_datetime = parse_html_datetime(request.form['start_date'])
    end_datetime = parse_html_datetime(request.form['end_date'])

    if start_datetime > end_datetime:
        flash('Aloitusajankohta ei voi olla päättymisajankohdan jälkeen.')
        return redirect('/transactions')

    duration = (end_datetime - start_datetime)
    duration_hours = (duration.seconds // 3600) + (duration.days * 24)

    for user in users:
        sql = '''
            INSERT INTO transactions (
                user_id, boat_id, created, usage_id, amount, start_date, end_date, description
                ) 
                VALUES (
                    :user_id, :boat_id, NOW(), 2, :duration_hours, :start_date, :end_date, :description
                    )
        '''

        # One hour of maintenance buys 3 hours of usage
        db.session.execute(sql, {
            'user_id': user, 'boat_id': session['boat']['id'], 'duration_hours': duration_hours,
            'start_date': start_datetime, 'end_date': end_datetime,
            'description': description
        })

        sql = '''
            UPDATE owners 
                SET usage_hours = usage_hours + :usage_hours_per_user 
                WHERE user_id = :user_id AND boat_id = :boat_id;
            '''
        db.session.execute(
            sql, {
                'usage_hours_per_user': duration_hours * 3,
                'user_id': user,
                'boat_id': session['boat']['id']
                }
            )

        db.session.commit()

    flash('Talkootyö lisätty.')
    return redirect('/transactions')


def addcost_view():
    amount = request.form['amount']
    cost_type = request.form['cost_type']
    description = request.form['description']

    if float(amount) <= 0:
        flash('Kulun on oltava suurempi kuin 0.')
        return redirect('/transactions')

    if not validate_length(description, 255):
        flash('Kulun kuvaus on liian pitkä.')
        return redirect('transactions/')

    start_datetime = parse_html_datetime(request.form['start_date'])
    end_datetime = start_datetime

    file = request.files['file']

    name = file.filename
    print(name)

    if (not name.endswith('.jpg')) and (not name.endswith('.png')):
        flash('Väärä tiedostomuoto. Kuittikuvan on oltava jpg tai png.')
        return redirect('/transactions')

    data = file.read()

    if len(data) > 800 * 1024:
        flash('Suurin tiedostokoko on 800KB')
        return redirect('/transactions')

    # usage id for cost = 3
    sql = '''
        INSERT INTO transactions (
            user_id, boat_id, created, usage_id, amount, start_date, end_date, description, cost_type_id, attachment_name, attachment_file
            ) 
            VALUES (
                :user_id, :boat_id, NOW(), 3, :amount, :start_date, :end_date, :description, :cost_type, :file_name, :file
                )
        '''

    db.session.execute(
        sql, {
            'user_id': session['user']['id'],
            'boat_id': session['boat']['id'],
            'amount':amount,
            'start_date': start_datetime,
            'end_date': end_datetime,
            'description': description,
            'cost_type': cost_type,
            'file_name': name,
            'file': data
            }
        )

    db.session.commit()

    flash('Kulu lisätty.')
    return redirect('/transactions')


def addincome_view():
    amount = request.form['amount']
    income_type = request.form['income_type']
    description = request.form['description']

    if float(amount) <= 0:
        flash('Tulon on oltava suurempi kuin 0.')
        return redirect('/transactions')

    if not validate_length(description, 255):
        flash('Kulun kuvaus on liian pitkä.')
        return redirect('transactions/')

    start_datetime = parse_html_datetime(request.form['start_date'])
    end_datetime = start_datetime

    # usage_id for income = 4
    sql = '''
        INSERT INTO transactions (
            user_id, boat_id, created, usage_id, amount, start_date, end_date, description, income_type_id
            ) 
            VALUES (
                :user_id, :boat_id, NOW(), 4, :amount, :start_date, :end_date, :description, :income_type
                )
        '''

    db.session.execute(
        sql, {
            'user_id': session['user']['id'],
            'boat_id': session['boat']['id'],
            'amount':amount,
            'start_date': start_datetime,
            'end_date': end_datetime,
            'description': description,
            'income_type': income_type
            }
        )

    db.session.commit()

    flash('Tulo lisätty.')
    return redirect('transactions')


def show_view(image_id):
    sql = '''
        SELECT boat_id, attachment_name FROM transactions WHERE id=:image_id
    '''

    result = db.session.execute(sql, {'image_id': image_id})
    db.session.commit()

    image_boat = result.fetchone()
    print(image_boat)

    if not image_boat or not image_boat[1]:
        return redirect('/transactions')

    image_boat = image_boat[0]

    if int(image_boat) != int(session['boat']['id']):
        return redirect('/transactions')

    sql = '''
        SELECT attachment_file FROM transactions WHERE id=:image_id
    '''

    result = db.session.execute(sql, {'image_id': image_id})
    db.session.commit()
    data = result.fetchone()[0]

    response = make_response(bytes(data))
    response.headers.set('Content-Type', 'image/jpeg')

    return response
