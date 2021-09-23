from flask import render_template


def manageboat_view(boat_id):
    # check that user is this boats admin
    print(boat_id)
    return render_template('manageboat.html')
    