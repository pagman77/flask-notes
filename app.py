"""Flask app for Notes"""
from click import password_option
from flask import Flask, jsonify, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import NewUserForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def hompage_redirect():
    """Redirect user to register user."""

    return redirect("/register")


@app.route('/register', methods=["GET", "POST"])
def register_new_user():
    """Display form, or accept submission for new user."""

    form = NewUserForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password, email=email,
            first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        session["username"] = username

        return redirect("/secret")

    else:
        return render_template("/register.html", form=form)