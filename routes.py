from app import app
from db import db
from flask import redirect, render_template, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from utils import login_required, validate_alphanum, validate_length, validate_year
from secrets import token_hex
from datetime import date

from views.index import index_view
from views.login import login_view, loginuser_view
from views.register import register_view, registeruser_view
from views.logout import logout_view
from views.boats import boats_view, addboat_view, joinboat_view


# TEMPLATES

# template for chart route
@app.route('/chart')
@login_required
def chart():
    labels = ['Tom', 'Dick', 'Harry']
    label = 'No. of things'
    data = [1, 3, 4]
    return render_template('chart.html', labels=labels, label=label, data=data)

# END TEMPLATES

@app.route('/')
@login_required
def index():
    return index_view()


@app.route('/login')
def login():
    return login_view()


@app.route('/loginuser', methods=['POST'])
def loginuser():
    return loginuser_view()


@app.route('/logout')
def logout():
    return logout_view()
    

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/registeruser', methods=['POST'])
def register_user():
    return registeruser_view()

    
@app.route('/boats')
@login_required
def boats():
    return boats_view()


@app.route('/addboat', methods=['POST'])
@login_required
def addboat():
    return addboat_view()
    

@app.route('/joinboat', methods=['POST'])
@login_required
def joinboat():
    return joinboat_view()