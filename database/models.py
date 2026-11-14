
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

from extensions import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.Date, nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Event {self.title}>"


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


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<Admin {self.username}>"


class Student(UserMixin, db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    notifications = db.relationship(
        "Notification",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student {self.email}>"


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    occurrence_id = db.Column(
    db.Integer,
    nullable=False,
    index=True
)

    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)

    notification_type = db.Column(
        db.String(30),
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    student = db.relationship(
        "Student",
        back_populates="notifications"
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "occurrence_id",
            "notification_type",
            name="uq_student_occurrence_notification"
        ),
    )

    def __repr__(self):
        return f"<Notification {self.title}>"
