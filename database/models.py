from flask_login import UserMixin
from datetime import datetime
from extensions import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    event_date = db.Column(db.Date, nullable=False)

    event_type = db.Column(db.String(50), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Event {self.title}>"


from datetime import datetime
from extensions import db


class DeletedEvent(db.Model):
    __tablename__ = "deleted_events"

    id = db.Column(db.Integer, primary_key=True)

    original_event_id = db.Column(db.Integer)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    event_date = db.Column(db.Date, nullable=False)

    event_type = db.Column(db.String(50), nullable=False)

    deleted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# ADMIN MODEL
class Admin(UserMixin, db.Model):

    __tablename__ = "admins"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<Admin {self.username}>"