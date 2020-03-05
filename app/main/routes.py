from flask import Flask, render_template, request, url_for, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required

from app.models import User, Transaction, Coin, db
from app.forms import TransactionForm

main = Blueprint('main', __name__)

def performTransaction(sender, recipient, coin, type):
    """ Adds a transaction to the database """

    transaction = Transaction(sender_id=sender.id, recipient_id=recipient.id, coin_id=coin.id, type=type)
    if type == 'Deducted':
        coin.owner_id = 1 # set coin owner back to admin (admin id is always 1)
    elif type == 'Awarded':
        coin.owner_id = recipient.id # set coin owner to student recieving coin
    db.session.add(transaction)
    db.session.add(coin)
    db.session.commit()

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/leaderboard', methods=['GET'])
def leaderboard():

    # get all students and reverse bubble sort by the number of coins they have
    users = User.query.filter(User.roles.any(name='Student')).order_by(User.username).all()
    n = len(users)
    for i in range(n):
        for j in range(0, n-1-i):
            if len(users[j+1].coins) > len(users[j].coins):
                users[j], users[j+1] = users[j+1], users[j]


    return render_template('leaderboard.html', users=users, n=n)

@main.route('/sendCoin', methods=['GET', 'POST'])
@roles_required('Teacher') # user must have teacher role to access this page
@login_required
def sendCoin():

    # load transaction form
    transaction_form = TransactionForm()
    # add all student instances to drop down table
    transaction_form.recipient.query = User.query.filter(User.roles.any(name='Student')).order_by(User.username)

    # get and validate transaction form data
    if transaction_form.validate_on_submit():
        recipient = transaction_form.recipient.data
        attitudeNum = transaction_form.attitudeNum.data

        # award student two coins
        if attitudeNum == '4':
            for i in range(2):
                # query db for coin instance owned by admin
                coin_obj = Coin.query.filter(Coin.owner_id==1).first()
                performTransaction(current_user, recipient, coin_obj, 'Awarded')

        # award student one coin
        elif attitudeNum == '3':
            coin_obj = Coin.query.filter(Coin.owner_id==1).first()
            performTransaction(current_user, recipient, coin_obj, 'Awarded')

        # deduct one coin
        elif attitudeNum == '2':
            # query db for coin owner by the student
            coin_obj = Coin.query.filter(Coin.owner_id==recipient.id).first()
            if coin_obj:
                performTransaction(recipient, current_user, coin_obj, 'Deducted')
            else:
                return 'Student has no coins'

        # deduct two coins
        elif attitudeNum == '1':
            for i in range(2):
                coin_obj = Coin.query.filter(Coin.owner_id==recipient.id).first()
                if coin_obj:
                    performTransaction(recipient, current_user, coin_obj, 'Deducted')
                else:
                    return 'Student has no coins'

    return render_template("transaction.html", form=transaction_form)


@main.route('/coinJar', methods=['GET'])
@roles_required('Student')
@login_required
def coinJar():

    # query db for all transactions regarding current user
    transactions = Transaction.query.filter((Transaction.recipient_id==current_user.id)|(Transaction.sender_id==current_user.id)).order_by(Transaction.timestamp).all()
    teachers = []
    types = []
    for i in transactions:
        # if awarded then sender id must be a teacher
        if i.type == 'Awarded':
            teachers.append(User.query.filter_by(User.id==i.sender_id).filter(User.roles.any(name='Teacher')).first())
        # if deducted sender if must be a student
        elif i.type == 'Deducted':
            teachers.append(User.query.filter_by(User.id==i.recipient_id).filter(User.roles.any(name='Teacher')).first())

        types.append(i.type)


    return render_template('coin_jar.html', transactions=transactions, teachers=teachers, types=types)
