from flask import Flask, render_template, request, url_for, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from app.forms import RegForm, LoginForm
from app.models import db, User, Role

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST', 'GET'])
def register():

    user_form = RegForm()

    if user_form.validate_on_submit():
        firstname = user_form.firstname.data
        lastname = user_form.lastname.data
        username = user_form.username.data
        role = user_form.role.data
        password = user_form.password.data

        # Check if username already exists
        user_obj = User.query.filter_by(username=username).first()
        if user_obj:
            return "Username taken"

        # Add user to database
        roleobj = Role.query.filter_by(name=role).first()
        if roleobj:
            user = User(firstname=firstname, lastname=lastname, username=username, password=password, roles=[roleobj])
            # user.roles.append(roleobj)
            db.session.add(user)
            db.session.commit()
        else:
            return role

        return redirect(url_for('auth.login'))

    return render_template('register.html', form=user_form)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow if login is validated successfully
    if login_form.validate_on_submit():
        user_obj = User.query.filter_by(username=login_form.username.data).first()
        if user_obj:
            login_user(user_obj)
            return redirect(url_for('main.coinJar'))
        else:
            return redirect(url_for('auth.login'))

    return render_template('login.html', form=login_form)


@auth.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('main.index'))
