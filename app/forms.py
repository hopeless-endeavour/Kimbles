from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, RadioField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from .models import User


def invalid_creds(form, field):
    """ Username and password validator """

    input_username = form.username.data
    input_password = field.data

    # search db for corresponding username
    user_obj = User.query.filter_by(username=input_username).first()

    # validate user
    if user_obj:
        user = user_obj
    else:
        raise ValidationError("Username or password is incorrect")

    # validate password
    if input_password != user.password:
        raise ValidationError("Username or password is incorrect")


class RegForm(FlaskForm):
    """ Registraion Form """

    firstname = StringField('firstName_label',
        validators=[InputRequired(message="First Name required"),
        Length(min=4, max=25, message="First name must be between 4 and 25\
        characters")])
    lastname = StringField('lastName_label',
        validators=[InputRequired(message="Last Name required"),
        Length(min=4, max=25, message="Last name must be between 4 and 25\
        characters")])
    username = StringField('username_label',
        validators=[InputRequired(message="Username required"),
        Length(min=4, max=25, message="Username must be between 4 and 25\
        characters")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"),
        Length(min=8, max=25, message="Password must be between 8 and 25\
        characters")])
    role = RadioField('role_label', choices=[('Teacher', 'Teacher'), ('Student', 'Student')], validators=[InputRequired()])
    confirm_pswd = PasswordField('confirm_pswd_label',
        validators=[InputRequired(message="Password required"),
        EqualTo('password', message="Password must match")])
    submit_button = SubmitField('Submit')


class LoginForm(FlaskForm):
    """ Login Form """

    username = StringField('username_label',
        validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"), invalid_creds])
    submit_button = SubmitField('Submit')


class TransactionForm(FlaskForm):
    """ Coin Transaction Form """

    recipient = QuerySelectField('recipient_label', get_label='username', allow_blank=True,
        validators=[InputRequired(message="Student username required")])
    attitudeNum = RadioField('attitudeNum_label', choices=[('1', 'One'),('2','Two'), ('3','Three'), ('4','Four')], validators=[InputRequired()])

    submit_button = SubmitField('Submit')
