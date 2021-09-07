from flask import Flask, redirect, render_template, session, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from os import getenv

app = Flask(__name__)

app.secret_key = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///kimppavene"
db = SQLAlchemy(app)


@app.route('/')
def index(alert_message):
    return render_template('index.html')


@app.route('/login')
def login():
    
    # if a user is logged in, we redirect to index
    try:
        current_user = session['user']
        return redirect('/')
    except(KeyError):
        return render_template('login.html')

@app.route('/loginuser', methods=['POST'])
def loginuser():
    username = request.form['username']
    password = request.form['password']
    alert_message = 'Virheellinen käyttäjänimi tai salasana'
        
    # get user
    sql = 'SELECT * FROM users WHERE username=:username'
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        return render_template("login.html", alert_message=alert_message)
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session['user'] = {
                                'username': user.username, 
                                'id': user.id, 
                                'first_name': user.first_name, 
                                'last_name': user.last_name
                                }
            return redirect('/')
        else:
            return render_template('/login', alert_message=alert_message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
