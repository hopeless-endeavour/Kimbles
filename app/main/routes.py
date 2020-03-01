from flask import Flask, render_template, request, url_for, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from app.models import User, Transaction, Coin, db
from app.forms import TransactionForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/leaderboard', methods=['GET'])
def leaderboard():

    users = User.query.all()
    students = [i for i in users if i.has_role('Student')]

    return render_template('leaderboard.html', students=students)

@main.route('/sendCoin', methods=['GET', 'POST'])
@login_required
def sendCoin():

    transaction_form = TransactionForm()
    transaction_form.recipient.query = User.query.filter(User.has_role('Student')).order_by(User.username)

    if transaction_form.validate_on_submit():
        recipient = transaction_form.recipient.data
        attitudeNum = transaction_form.attitudeNum.data

        # recipient = User.query.filter_by(id=recipient.id).first()

        if attitudeNum == '4':
            coin = Coin.query.filter_by(owner_id=1).first()
            transaction = Transaction(sender_id=current_user.id, recipient_id=recipient.id, coin_id=coin.id)
            coin.owner_id = recipient.id
            db.session.add(transaction)
            db.session.add(coin)
            db.session.commit()

            return "Successful Transaction"

    return render_template("transaction.html", form=transaction_form)


@main.route('/coinJar', methods=['GET'])
@login_required
def coinJar():

    numofCoins = len(current_user.coins)
    transactions = Transaction.query.filter_by(recipient_id=current_user.id).all()

    return render_template('coin_jar.html', transactions=transactions, numofCoins=numofCoins)
