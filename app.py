import os

from flask import Flask, render_template, request, url_for, redirect

from wtform_fields import *
from models import *

# App configuration
app = Flask(__name__)
app.secret_key = 'secret key'

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://ysfcykvennnxov:e911f42296ffa7b2d0477cc1fd60bb248ad149ee6e1513a9fe52e9f84ce57a7c@ec2-54-228-243-238.eu-west-1.compute.amazonaws.com:5432/depivghlt560jh'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/registerStudent', methods=['POST', 'GET'])
def registerStudent():

    student_form = StudentReg()

    if student_form.validate_on_submit():
        firstname = student_form.firstname.data
        lastname = student_form.lastname.data
        classcode = student_form.classcode.data
        password = student_form.password.data
        username = lastname[:3] + firstname[:3]

        # Check username exists
        user_object = Student.query.filter_by(username=username).first()
        if user_object:
            return "Username taken"

        # Add student to database
        student = Student(firstname=firstname, lastname=lastname, username=username, classcode=classcode, password=password)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('reg_student.html', form=student_form)


@app.route('/registerTeacher', methods=['POST', 'GET'])
def registerTeacher():

    teacher_form = TeacherReg()

    if teacher_form.validate_on_submit():
        firstname = teacher_form.firstname.data
        lastname = teacher_form.lastname.data
        password = teacher_form.password.data
        username = firstname[0] + lastname

        # Check username exists
        user_object = Teacher.query.filter_by(username=username).first()
        if user_object:
            return "Username taken"

        # Add student to database
        teacher = Teacher(firstname=firstname, lastname=lastname, username=username, password=password)
        db.session.add(teacher)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('reg_teacher.html', form=teacher_form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow if login is validated successfully
    if login_form.validate_on_submit():
        return "Logged in"

    return render_template("login.html", form=login_form)


@app.route('/sendToken', methods=['GET', 'POST'])
def sendToken():

    transaction_form = TransactionForm()

    if transaction_form.validate_on_submit():
        sender = transaction_form.sender.data
        recipient = transaction_form.recipient.data
        amount = transaction_form.amount.data

        sender_id = Teacher.query.filter_by(username=sender).first()
        recipient_id = Student.query.filter_by(username=recipient).first()

        transaction = Transaction(sender=sender_id.id, recipient=recipient_id.id, amount=amount)
        db.session.add(transaction)
        db.session.commit()

        return "Successful Transaction"

    return render_template("transaction.html", form=transaction_form)

if __name__ == '__main__':
    app.run(debug=True)
