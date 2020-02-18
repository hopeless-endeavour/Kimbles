from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """ Student Model """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(6), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')
    coins = db.relationship('Coin', backref='owner')

class Role(db.Model):
    """ Role Model """
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    """ Association table for many to many relationship between users and roles """

    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Transaction(db.Model):
    """ Transaction Model """

    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    coin_id = db.Column(db.Integer, db.ForeignKey("coins.id"))
    timestamp =db.Column(db.DateTime, default=datetime.now())

class Coin(db.Model):
    """ Coin Model """

    __tablename__ = 'coins'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
