from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()]
                        )

    username = StringField('User name',
                           validators=
                           [
                               DataRequired(),
                               Length(1, 64),
                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                      0, 'User names must have only '
                                      'letters, numbers, dots or '
                                      'underscores.'
                                      )
                           ]
                           )

    password = PasswordField('Password',
                             validators=
                             [
                                DataRequired(),
                                EqualTo('password2', message='Passwords must match.')
                             ]
                             )

    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    submit = SubmitField('Register')

    # Custom validator implemented as methods.
    # When a form defines a method with the prefix 'validate_' followed by the
    #  name of a field, the method is invoked in addition to any regularly
    #  defined validators.
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePwdForm(FlaskForm):
    old_pwd = PasswordField('Old Password', validators=[DataRequired()])
    new_pwd = PasswordField('New Password', validators=[DataRequired(),
                                                        EqualTo('new_pwd2', message='Passwords must match.')])
    new_pwd2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')
