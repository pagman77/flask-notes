"""Models for Notes app."""
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Creates user."""

    __tablename__ = "users"

    def __repr__(self):
        """Show info about user."""

        u = self

        return f"<{u.first_name} {u.last_name} has username of\
            {u.username} and email is {u.email}>"

    username = db.Column(db.String(20), primary_key=True)

    password = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    notes = db.relationship("Note", backref='users')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Registers the user on the class and hashes password."""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username, password=hashed, email=email,
            first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and has correct password."""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Note(db.Model):
    """Creates user."""

    __tablename__ = "notes"

    def __repr__(self):
        """Show info about user."""

        n = self

        return f"<{n.title} {n.id} has owner of {n.owner}>"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    owner = db.Column(db.Text, db.ForeignKey('users.username'), nullable=False)





