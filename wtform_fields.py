from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegForm(FlaskForm):
    """ Registraion form """

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
