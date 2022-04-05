from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    """Form for adding new user."""

    username = StringField("Username: ", validators=[InputRequired(), Length(20)])

    password = StringField("Password: ", validators=[InputRequired(), Length(100)])

    email = StringField("Email: ", validators=[InputRequired(), Length(50)])

    first_name = StringField("First name: ", validators=[InputRequired(), Length(30)])

    last_name = StringField("Last name:", validators=[InputRequired(), Length(30)])

class LoginForm(FlaskForm):
    """Form for logging in."""

    username = StringField("Username: ", validators=[InputRequired(), Length(20)])

    password = StringField("Password: ", validators=[InputRequired(), Length(100)])