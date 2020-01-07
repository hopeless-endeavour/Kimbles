from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
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
        raise ValidationError("Username or password is incorrect")

    # validate password
    if input_password != user.password:
        raise ValidationError("Username or password is incorrect")


def validate_transaction(form, field):
    """ Validates sender and recipient of transaction """

    input_sender = form.sender.data
    input_recipient = field.data

    # search db for corresponding sender
    sender_object = Teacher.query.filter_by(username=input_sender).first()
    recipient_object = Student.query.filter_by(username=input_recipient).first()

    if sender_object is None or recipient_object is None:
        raise ValidationError("Sender or recipient does not exist")


class StudentReg(FlaskForm):
    """ Student Registraion Form """

    firstname = StringField('firstName_label',
        validators=[InputRequired(message="First Name required"),
        Length(min=4, max=25, message="First name must be between 4 and 25\
        characters")])
    lastname = StringField('lastName_label',
        validators=[InputRequired(message="Last Name required"),
        Length(min=4, max=25, message="Last name must be between 4 and 25\
        characters")])
    classcode = StringField('classCode_label',
        validators=[InputRequired(message="Class Code required"),
        Length(3, message="Class code must be 3 characters long")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"),
        Length(min=4, max=25, message="Password must be between 4 and 25\
        characters")])
    confirm_pswd = PasswordField('confirm_pswd_label',
        validators=[InputRequired(message="Password required"),
        EqualTo('password', message="Password must match")])
    submit_button = SubmitField('Create')


class TeacherReg(FlaskForm):
    """ Teacher Registration Form """

    firstname = StringField('firstName_label',
        validators=[InputRequired(message="First Name required"),
        Length(min=4, max=25, message="First name must be between 4 and 25\
        characters")])
    lastname = StringField('lastName_label',
        validators=[InputRequired(message="Last Name required"),
        Length(min=4, max=25, message="Last name must be between 4 and 25\
        characters")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"),
        Length(min=4, max=25, message="Password must be between 4 and 25\
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


class TransactionForm(FlaskForm):
    """ Token Transaction Form """

    sender = StringField('sender_label',
        validators=[InputRequired(message="Sender username required")])
    recipient = StringField('recipient_label',
        validators=[InputRequired(message="Recipient username required"), validate_transaction])
    amount = IntegerField('recipient_label',
        validators=[InputRequired(message="Amount required")])
    submit_button = SubmitField('Send')
