"""Flask app for Notes"""
from click import password_option
from flask import Flask, jsonify, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, NoteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notely'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

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

        return redirect(f"/users/{username}")

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


@app.get("/users/<user_name>")
def user_page(user_name):
    """check for username"""

    form = CSRFProtectForm()

    if session.get("username") == user_name:
        user = User.query.get_or_404(user_name)
        notes = user.notes

        return render_template("user.html", user=user, form=form, notes=notes)
    else:
        flash("You're not authorized to view this page, punk.")
        return redirect("/login")


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect("/")


@app.delete("/user/<username>/delete")
def delete_post(username):
    """deletes all notes and then delete user from db"""
    
    form = CSRFProtectForm()

    if form.validate_on_submit():
        user = User.query.get_or_404(username)
        Note.query.fiter_by(owner=username).delete()
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        session.pop("username", None)
    return redirect("/")

@app.route("/user/<username>/notes/add", methods=["GET","POST"])
def add_note(username):
    """Display form, or accept submission for new note."""
        
    form = NoteForm()

    if session.get("username") == username:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            

            note = Note(title=title, content=content)

            db.session.add(note)
            db.session.commit()
            return redirect(f"/user/{username}")
        
        else:
            return render_template("add-note.html", form=form, username=username)
    flash("unauthorized")
    return redirect("/")
    
@app.route("/notes/<int:note_id>/update", methods=["GET","POST"])
def edit_note(note_id):
    """Display edit form, or accept submission for edit note."""
    curr_note = Note.query.get_or_404(note_id)
    form = NoteForm(obj=curr_note)
    username = curr_note.username

    if session.get("username") == username:
        if form.validate_on_submit():
            curr_note.title = form.title.data
            curr_note.content = form.content.data

            db.session.commit()
            flash("Successfully updated note!")
            return redirect(f"/user/{username}")
        
        else:
            return render_template("edit-note.html", form=form, username=username)
    flash("unauthorized, you kid")
    return redirect("/")




# For each note, display with a link to a form to edit the note and a button to delete the note.

# Have a link that sends you to a form to add more notes and a button to delete the entire user account, including their notes.

# POST /users/<username>/delete
# Remove the user from the database and make sure to also delete all of their notes. Clear any user information in the session and redirect to /.

# As with the logout route, make sure you have CSRF protection for this.

# GET /users/<username>/notes/add
# Display a form to add notes.
# POST /users/<username>/notes/add
# Add a new note and redirect to /users/<username>
# GET /notes/<note-id>/update
# Display a form to edit a note.
# POST /notes/<note-id>/update
# Update a note and redirect to /users/<username>.
# POST /notes/<note-id>/delete
# Delete a note and redirect to /users/<username>.

# As with the logout and delete routes, make sure you have CSRF protection for this.