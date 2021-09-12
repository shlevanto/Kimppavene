from flask import render_template

def manageboat_view(id):
    # check that user is this boats admin
    print(id)
    return render_template('manageboat.html')