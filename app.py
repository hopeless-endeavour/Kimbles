import os

from flask import Flask, render_template, request

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
        return "Student added"

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
        user_object = Student.query.filter_by(username=username).first()
        if user_object:
            return "Username taken"

        # Add student to database
        teacher = Teacher(firstname=firstname, lastname=lastname, username=username, password=password)
        db.session.add(teacher)
        db.session.commit()
        return "Teacher added"

    return render_template('reg_teacher.html', form=teacher_form)

@app.route('/login')
def login():
    pass

if __name__ == '__main__':
    app.run(debug=True)
