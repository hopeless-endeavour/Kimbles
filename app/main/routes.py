from flask import Flask, render_template, request, url_for, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_

from app.models import User, Transaction, Coin, db
from app.forms import TransactionForm

main = Blueprint('main', __name__)

def performTransaction(sender, recipient, coin):
    transaction = Transaction(sender_id=sender.id, recipient_id=recipient.id, coin_id=coin.id)
    coin.owner_id = recipient.id
    db.session.add(transaction)
    db.session.add(coin)
    db.session.commit()

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/leaderboard', methods=['GET'])
def leaderboard():

    users = User.query.all()
    n = len(users)
    for i in range(n):
        for j in range(0, n-1-i):
            if len(users[j].coins) > len(users[j+1].coins):
                users[j], users[j+1] = users[j+1], users[j]


    return render_template('leaderboard.html', users=users)

@main.route('/sendCoin', methods=['GET', 'POST'])
@login_required
def sendCoin():

    transaction_form = TransactionForm()
    transaction_form.recipient.query = User.query.order_by(User.username)

    if transaction_form.validate_on_submit():
        recipient = transaction_form.recipient.data
        attitudeNum = transaction_form.attitudeNum.data

        if attitudeNum == '4':
            coin_obj = Coin.query.filter(or_(Coin.owner_id==1, Coin.owner_id==current_user.id)).first()
            performTransaction(current_user, recipient, coin_obj)
        elif attitudeNum == '2':
            coin_obj = Coin.query.filter(Coin.owner_id==recipient.id).first()
            if coin_obj:
                performTransaction(sender=recipient, recipient=current_user, coin=coin_obj)
            else:
                return 'Student has no coins'
        elif attitudeNum == '1':
            for i in range(2):
                coin_obj = Coin.query.filter(Coin.owner_id==recipient.id).first()
                if coin_obj:
                    performTransaction(sender=recipient, recipient=current_user, coin=coin_obj)
                else:
                    return 'Student has no coins'

    return render_template("transaction.html", form=transaction_form)


@main.route('/coinJar', methods=['GET'])
@login_required
def coinJar():

    numofCoins = len(current_user.coins)
    transactions = Transaction.query.filter_by(recipient_id=current_user.id).order_by(Transaction.timestamp).all()
    length = len(transactions)
    senders = []
    status = []
    for i in transactions:
        senders.append(User.query.filter(User.id==i.sender_id).first())
        if current_user.id == i.recipient_id:
            status.append('Awarded')
        elif current_user.id == i.sender_id:
            status.append('Deducted')


    return render_template('coin_jar.html', transactions=transactions, length=length, numofCoins=numofCoins, senders=senders, status=status)
