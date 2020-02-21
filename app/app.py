import os

from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_user import roles_required, UserManager
from flask_sqlalchemy import SQLAlchemy

from wtform_fields import *
from models import db, User, Coin, Transaction, Role

# Create app
app = Flask(__name__)

# Config app according to stage
if app.config["ENV"] == "production":
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# Initiliase database
db.init_app(app)

@app.cli.command('createdb')
def create():
    """ CLI command to create db tables (flask createdb) """

    db.create_all()

@app.cli.command("create_sampledb")
def create_sampledb_cmd():
    """ CLI command to insert sample data into db (flask create_sampledb) """

    firstnames = ['Clarissa', 'Lucas', 'Jack', 'Lewis']
    lastnames = ['Brown', 'Jones', 'Smith', 'Thomas']
    usernames = ['BroCla', 'JonLuc', 'SmiJac', 'ThoLew']
    pwd = 'test'
    roles = ['Student', 'Teacher', 'Admin', 'Vendor']

    for i in range(0, len(roles)):
        role_name = Role(name=roles[i])
        db.session.add(role_name)
        db.session.commit()

    r = db.session.query(Role).all()
    for i in range(0, len(firstnames)):
        user = User(firstname=firstnames[i], lastname=lastnames[i], username=usernames[i], password=pwd)
        user.roles = [r[i]]
        db.session.add(user)
        db.session.commit()

    for i in range(10):
        coin = Coin()
        db.session.add(coin)
        db.session.commit()

@app.cli.command("cleardb")
def cleardb_cmd():
    """ CLI command to clear all data from all tables in db (flask cleardb) """

    for table in db.metadata.sorted_tables:
        db.session.execute(table.delete())
    db.session.commit()

# Flask login configuration
login = LoginManager(app)
login.init_app(app)
user_manager = UserManager(app, db, User)

@login.user_loader
def load_user(id):

    return User.query.get(int(id))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    pass

@app.route('/register', methods=['POST', 'GET'])
def register():

    user_form = UserReg()

    if user_form.validate_on_submit():
        firstname = user_form.firstname.data
        lastname = user_form.lastname.data
        role = user_form.role.data
        password = user_form.password.data
        username = lastname[:3] + firstname[:3] # creates username with format eg. John Smith -> SmiJon

        # Check if username already exists
        user_obj = User.query.filter_by(username=username).first()
        if user_obj:
            return "Username taken"

        # Check if role exists - change later
        roles = [r.name for r in Role.query.all()]
        if role not in roles:
            return "No such role"

        # Add user to database
        user = User(firstname=firstname, lastname=lastname, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', form=user_form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow if login is validated successfully
    if login_form.validate_on_submit():
        user_obj = User.query.filter_by(username=login_form.username.data).first()
        if user_obj is not None:
            login_user(user_obj)
            return redirect(url_for('coinJar'))

    return render_template("login.html", form=login_form)


@app.route('/sendCoin', methods=['GET', 'POST'])
@login_required
def sendCoin():

    transaction_form = TransactionForm()

    if transaction_form.validate_on_submit():
        sender_id = current_user.id
        recipient = transaction_form.recipient.data
        attitudeNum = transaction_form.attitudeNum.data

        recipient_id = User.query.filter_by(username=recipient).first()

        if attitudeNum == 4:
            coins = 1
        elif attitudeNum == 2:
            coins = -1
        elif attitudeNum == 1:
            coins = -2

        transaction = Transaction(sender=sender_id, recipient=recipient_id)
        db.session.query(User).filter(User.id == recipient_id.id).update({'coins': (User.coins + amount)})
        db.session.add(transaction)
        db.session.commit()

        return "Successful Transaction"

    return render_template("transaction.html", form=transaction_form)


@app.route('/coinJar', methods=['GET'])
@login_required
def coinJar():

    numofCoins = len(current_user.coins)
    transactions = Transaction.query.filter_by(recipient_id=current_user.id).all()

    return render_template('coin_jar.html', transactions=transactions, numofCoins=numofCoins)


@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
