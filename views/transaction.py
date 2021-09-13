from flask import render_template, request, redirect


def transaction_view():
    return render_template('transactions.html')


def addtransaction_view():
    # if users is empty, rerender with error message
    # if both durations are empty, rerender with error message
    users = request.form.getlist('user')
    return redirect('/transactions')
