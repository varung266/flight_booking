from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class SearchForm(FlaskForm):
    departure_time = DateTimeField('Departure Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Search')
