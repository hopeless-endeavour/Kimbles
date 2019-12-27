from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from models import Teacher, Student


def invalid_creds(form, field):
    """ Username and password validator """

    input_username = form.username.data
    input_password = field.data

    # search db for corresponding username
    teacher_object = Teacher.query.filter_by(username=input_username).first()
    student_object = Student.query.filter_by(username=input_username).first()

    # validate user
    if student_object:
        user = student_object
    elif teacher_object:
        user = teacher_object
    else:
        raise ValidationError("User does not exist")

    # validate password
    if input_password != user.password:
        raise ValidationError("Password is incorrect")
        # change to generic 'Username or password incorrect' for imporved security

class StudentReg(FlaskForm):
    """ Student Registraion Form """

    firstname = StringField('firstName_label',
        validators=[InputRequired(message="First Name required"),
        Length(min=4, max=25, message="First name must be between 5 and 25\
        characters")])
    lastname = StringField('lastName_label',
        validators=[InputRequired(message="Last Name required"),
        Length(min=4, max=25, message="Last name must be between 5 and 25\
        characters")])
    classcode = StringField('classCode_label',
        validators=[InputRequired(message="Class Code required"),
        Length(3, message="Class code must be 3 characters long")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"),
        Length(min=4, max=25, message="Password must be between 5 and 25\
        characters")])
    confirm_pswd = PasswordField('confirm_pswd_label',
        validators=[InputRequired(message="Password required"),
        EqualTo('password', message="Password must match")])
    submit_button = SubmitField('Create')


class TeacherReg(FlaskForm):
    """ Teacher Registration Form """

    firstname = StringField('firstName_label',
        validators=[InputRequired(message="First Name required"),
        Length(min=4, max=25, message="First name must be between 5 and 25\
        characters")])
    lastname = StringField('lastName_label',
        validators=[InputRequired(message="Last Name required"),
        Length(min=4, max=25, message="Last name must be between 5 and 25\
        characters")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"),
        Length(min=4, max=25, message="Password must be between 5 and 25\
        characters")])
    confirm_pswd = PasswordField('confirm_pswd_label',
        validators=[InputRequired(message="Password required"),
        EqualTo('password', message="Password must match")])
    submit_button = SubmitField('Create')


class LoginForm(FlaskForm):
    """ Login Form """

    username = StringField('username_label',
        validators=[InputRequired(message="Usernmae required")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"), invalid_creds])
    submit_button = SubmitField('Login')
