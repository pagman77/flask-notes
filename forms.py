from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    """Form for adding new user."""

    username = StringField("Username: ",
        validators=[InputRequired(), Length(max=20)])

    password = PasswordField("Password: ",
        validators=[InputRequired(), Length(max=100)])

    email = StringField("Email: ",
        validators=[InputRequired(), Length(max=50)])

    first_name = StringField("First name: ",
        validators=[InputRequired(), Length(max=30)])

    last_name = StringField("Last name:",
        validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    """Form for logging in."""

    username = StringField("Username: ",
        validators=[InputRequired(), Length(max=20)])

    password = PasswordField("Password: ",
        validators=[InputRequired(), Length(max=100)])

class CSRFProtectForm(FlaskForm):
    """CSRF protection"""
