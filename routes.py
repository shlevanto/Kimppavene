from app import app
from utils import login_required, boat_required

from views.index import index_view
from views.login import login_view, loginuser_view
from views.register import register_view, registeruser_view
from views.logout import logout_view
from views.boats import boats_view, addboat_view, joinboat_view, chooseboat_view
from views.manageboat import manageboat_view
from views.transactions import transactions_view, addusage_view, addmaintenance_view, addcost_view


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
    return addboat_view()
    

@app.route('/joinboat', methods=['POST'])
@login_required
def joinboat():
    return joinboat_view()


@app.route('/manageboat/<int:id>', methods=['GET'])
@login_required
def manageboat(id):
    return manageboat_view(id)


@app.route('/chooseboat', methods=['POST'])
@login_required
def chooseboat():
    return chooseboat_view()


@app.route('/transactions')
@login_required
def transactions():
    return transactions_view()


@app.route('/addusage', methods=['POST'])
@login_required
def addtransaction():
    return addusage_view()


@app.route('/addmaintenance', methods=['POST'])
@login_required
def addmaintenance():
    return addmaintenance_view()


@app.route('/addcost', methods=['POST'])
@login_required
def addcost():
    return addcost_view()