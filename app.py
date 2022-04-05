"""Flask app for Notes"""
from click import password_option
from flask import Flask, jsonify, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notely'
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

    form = RegisterForm()

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
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET","POST"])
def login_user():
    """Display form, or accept submission for login user."""

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data


        user = User.authenticate(username=username, password=password)

        if user:
            session["username"] = username # keep logged in
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


# GET /secret
# Return the text “You made it!” (don’t worry, we’ll get rid of this soon)

@app.get("/secret")
def login_page():
    """check for username"""

    if session["username"]:
        return render_template("user.html")
    else:
        flash("You're not authorized to view this page, punk.")
        return redirect("/login")


