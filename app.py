from flask import Flask, redirect, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from os import getenv

app = Flask(__name__)

app.secret_key = getenv('SECRET_KEY')

@app.route('/')
def index():
    return 'Tervetuloa Kimppaveneeseen'

@app.route('/login')
def login():
    # if a user is logged in, we redirect to index
    try:
        current_user = session['user']
    except(KeyError):
        return render_template('login.html')
    return ''