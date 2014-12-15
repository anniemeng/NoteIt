from flask.ext.wtf import Form
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    )
from wtforms.validators import Required, Length, Email, EqualTo


class LoginForm(Form):
    email = StringField('Email', validators=[Required(),
                                             Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    login = SubmitField('Log in')


class SignupForm(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Enter a password:',
                             validators=[Required(),
                                         EqualTo('password2',
                                         message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    signup = SubmitField('Sign up')


class DocumentForm(Form):
    title = StringField('Title', validators=[Required()])
    descrip = StringField('Description', validators=[Required()])
    url = StringField('URL', validators=[Required()])
    urlSub = SubmitField('Take notes!')


class NoteForm(Form):
    note = TextAreaField('Enter your note', validators=[Required()])
    highlight = TextAreaField(validators=[Required()])
    submit = SubmitField('Submit')
