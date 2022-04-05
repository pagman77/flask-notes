"""Flask app for Notes"""
from click import password_option
from flask import Flask, jsonify, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

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

        return redirect(f"/user/{username}")

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
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


# GET /secret
# Return the text “You made it!” (don’t worry, we’ll get rid of this soon)

@app.get("/users/<int:user_name>")
def login_page(user_name):
    """check for username"""

    if session["username"]:
        user = User.query.get_or_404(user_name)
        
        return render_template("user.html", user=user)
    else:
        flash("You're not authorized to view this page, punk.")
        return redirect("/login")




@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "user_id" if present, but no errors if it wasn't
        session.pop("username", None)

    return redirect("/")
