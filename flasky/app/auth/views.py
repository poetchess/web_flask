from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegistrationForm, ChangePwdForm, ForgetPwdForm, ResetPwdForm
from .. import db
from ..models import User
from ..email import send_email


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
            # return redirect(request.args.get('next') or url_for('main.index'))
            return redirect(url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, 
                    username=form.username.data,
                    password=form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


# This route is protected with 'login_required' to ensure that when it is
# accessed, the user that is making the request is known.
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


# From a blueprint, the 'before_request' hook applies only to requests that
# belong to the blueprint. To install a hook for all application requests from
# a blueprint, use'before_app_request'
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you.')
    return redirect(url_for('main.index'))


@auth.route('/change_pwd', methods=['GET', 'POST'])
@login_required
def change_pwd():
    form = ChangePwdForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_pwd.data):
            current_user.password = form.new_pwd.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        flash('Old password is not correct.')

    return render_template('auth/change_pwd.html', form=form)


@auth.route('/forget_pwd', methods=['GET', 'POST'])
def forget_pwd():
    form = ForgetPwdForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('User does not exist.')
        else:
            token = User.generate_reset_pwd_token(form.email.data)
            send_email(user.email, 'Reset Your Password', 'auth/email/reset_pwd', user=user, token=token)
            flash('An email has been sent to you to reset the password.')
            return redirect(url_for('main.index'))
    return render_template('auth/forget_pwd.html', form=form)


@auth.route('/reset_pwd/<token>', methods=['GET', 'POST'])
def reset_pwd(token):
    form = ResetPwdForm()
    if form.validate_on_submit():
        data = User.get_reset_pwd_token(token)
        try:
            email = data.get('confirm_email')
            user = User.query.filter_by(email=email).first()
            user.password = form.new_pwd.data
            db.session.add(user)
            flash('Successfully reset the password, please login with new password.')
        except:
            flash('Failed to reset password.')
        return redirect(url_for('main.index'))
    return render_template('auth/reset_pwd.html', form=form)
