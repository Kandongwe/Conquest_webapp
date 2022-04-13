# Creating user sing up form and login forms
from flask_wtf import flaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo, Email


# Class for registration/sign up form
class RegistrationForm(flaskForm):
    username = StringField(label="username", validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField(label="email", validators=[DataRequired(), Email()])
    password = PasswordField(label="password", validators=[DataRequired(), Length(min=6, max=16)])
    comfirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(label="Sign up")

#class for login form
class LoginForm(flaskForm):
    email = StringField(label="email", validators=[DataRequired(), Email()])
    password = PasswordField(label="password", validators=[DataRequired(), Length(min=6, max=16)])
    submit = SubmitField(label="Login")