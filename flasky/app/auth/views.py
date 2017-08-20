from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # If the login form was presented to the user to prevent unauthorized
            # access to a protected URL, then flask_login saved the original URL
            # in the 'next' query string argument, which can be accessed from the
            # request.args dictionary. If the 'next' query string argument is not
            # available, a redirect to the home page is issued instead.
            #return redirect(request.args.get('next') or url_for('main.index'))
            return redirect(url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))