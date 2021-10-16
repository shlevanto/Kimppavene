from flask import request

from app import app
from utils import login_required, csrf

from views.index import index_view
from views.login import login_view, loginuser_view
from views.register import register_view, registeruser_view
from views.logout import logout_view
from views.boats import boats_view, addboat_view, joinboat_view, chooseboat_view
from views.manageboat import manageboat_view, editboat_view, editboatadmins_view, edittimerates_view
from views.transactions import (
    transactions_view, addusage_view,
    addmaintenance_view, addcost_view, addincome_view, show_view
    )


@app.route('/', methods=['GET'])
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
    return register_view()


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
    csrf(request.form['csrf_token'])
    return addboat_view()


@app.route('/joinboat', methods=['POST'])
@login_required
def joinboat():
    csrf(request.form['csrf_token'])
    return joinboat_view()


@app.route('/manageboat')
@login_required
def manageboat():
    return manageboat_view()


@app.route('/chooseboat', methods=['POST'])
@login_required
def chooseboat():
    csrf(request.form['csrf_token'])
    return chooseboat_view()


@app.route('/transactions', methods=['GET'])
@login_required
def transactions():
    return transactions_view()


@app.route('/addusage', methods=['POST'])
@login_required
def addtransaction():
    csrf(request.form['csrf_token'])
    return addusage_view()


@app.route('/addmaintenance', methods=['POST'])
@login_required
def addmaintenance():
    csrf(request.form['csrf_token'])
    return addmaintenance_view()


@app.route('/addcost', methods=['POST'])
@login_required
def addcost():
    csrf(request.form['csrf_token'])
    return addcost_view()


@app.route('/addincome', methods=['POST'])
@login_required
def addincome():
    csrf(request.form['csrf_token'])
    return addincome_view()


@app.route('/editboat', methods=['POST'])
@login_required
def editboat():
    csrf(request.form['csrf_token'])
    return editboat_view()


@app.route('/editboatadmins', methods=['POST'])
@login_required
def editboatadmins():
    csrf(request.form['csrf_token'])
    return editboatadmins_view()


@app.route('/edittimerates', methods=['POST'])
@login_required
def edittimerates():
    csrf(request.form['csrf_token'])
    return edittimerates_view()


@app.route('/show/<int:id>')
@login_required
def show(id):
    return show_view(id)
