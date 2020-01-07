from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Student(UserMixin, db.Model):
    """ Student Model """

    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(6), nullable=False)
    classcode = db.Column(db.String(25), nullable=False)
    tokens = db.Column(db.Integer, default=0)
    password = db.Column(db.String(25), nullable=False)

    # def __repr__(self):
    #     return "<Student(firstName='{}', lastName='{}', classCode='{}')>"\
    #             .format(self.firstName, self.lastName, self.classCode)


class Teacher(UserMixin, db.Model):
    """ Teacher Model """

    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    username = db.Column(db.String(6), nullable=False)
    password = db.Column(db.String(25), nullable=False)

    # def __repr__(self):
    #     return "<Teacher(firstName='{}', lastName='{}')>"\
    #             .format(self.firstName, self.lastName)


class Transaction(db.Model):
    """ Transaction Model """

    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String, db.ForeignKey("teachers.id"))
    recipient = db.Column(db.String, db.ForeignKey("students.id"))
    amount = db.Column(db.Integer)
    timestamp =db.Column(db.DateTime, default=datetime.now())

    # def __repr__(self):
    #     return "<Transaction(sender='{} recipient='{}', amount='{}')>"\
    #             .format(self.sender, self.recipient, self.amount)
