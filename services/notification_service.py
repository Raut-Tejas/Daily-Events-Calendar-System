
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from extensions import db
from database.models import Notification


def create_notification(
    student_id,
    occurrence_id,
    title,
    message,
    notification_type="event_reminder"
):
    """
    Create an in-app notification for a student.
    Duplicate notifications are prevented by the database constraint.
    """

    notification = Notification(
        student_id=student_id,
        occurrence_id=occurrence_id,
        title=title,
        message=message,
        notification_type=notification_type,
        is_read=False,
        created_at=datetime.utcnow()
    )

    try:
        db.session.add(notification)
        db.session.commit()
        return notification

    except IntegrityError:
        db.session.rollback()
        return None


def get_student_notifications(student_id, limit=50):
    """Return the latest notifications for a student."""

    return (
        Notification.query
        .filter_by(student_id=student_id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
        .all()
    )


def get_unread_count(student_id):
    """Return the number of unread notifications."""

    return Notification.query.filter_by(
        student_id=student_id,
        is_read=False
    ).count()


def mark_notification_as_read(notification_id, student_id):
    """Mark a notification as read only if it belongs to the student."""

    notification = Notification.query.filter_by(
        id=notification_id,
        student_id=student_id
    ).first()

    if notification is None:
        return False

    notification.is_read = True
    db.session.commit()

    return True


def mark_all_notifications_as_read(student_id):
    """Mark all notifications belonging to a student as read."""

    Notification.query.filter_by(
        student_id=student_id,
        is_read=False
    ).update(
        {"is_read": True},
        synchronize_session=False
    )

    db.session.commit()
