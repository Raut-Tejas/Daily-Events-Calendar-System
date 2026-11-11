
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
