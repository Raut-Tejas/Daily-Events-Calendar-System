
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

from database.models import Event
from extensions import db

event_bp = Blueprint("events", __name__)


# Display all events
@event_bp.route("/events")
def view_events():
    events = Event.query.order_by(Event.event_date.asc()).all()
    return render_template("events.html", events=events)


# Display add event form
@event_bp.route("/events/add", methods=["GET", "POST"])
def add_event():

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        event_date = request.form.get("event_date")
        event_type = request.form.get("event_type")

        if not title or not event_date or not event_type:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("events.add_event"))

        try:
            event_date = datetime.strptime(
                event_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            flash("Please enter a valid event date.", "error")
            return redirect(url_for("events.add_event"))

        new_event = Event(
            title=title,
            description=description,
            event_date=event_date,
            event_type=event_type
        )

        db.session.add(new_event)
        db.session.commit()

        flash("Event added successfully!", "success")
        return redirect(url_for("events.view_events"))

    return render_template("add_event.html")


# Edit existing event
@event_bp.route("/events/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):

    event = db.get_or_404(Event, event_id)

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        event_date = request.form.get("event_date")
        event_type = request.form.get("event_type")

        if not title or not event_date or not event_type:
            flash("Please fill in all required fields.", "error")
            return redirect(
                url_for("events.edit_event", event_id=event.id)
            )

        try:
            event_date = datetime.strptime(
                event_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            flash("Please enter a valid event date.", "error")
            return redirect(
                url_for("events.edit_event", event_id=event.id)
            )

        event.title = title
        event.description = description
        event.event_date = event_date
        event.event_type = event_type

        db.session.commit()

        flash("Event updated successfully!", "success")
        return redirect(url_for("events.view_events"))

    return render_template("edit_event.html", event=event)


# Delete an event

from database.models import Event, DeletedEvent
from extensions import db
from datetime import datetime


@event_bp.route("/events/delete/<int:event_id>", methods=["POST"])
def delete_event(event_id):

    event = db.get_or_404(Event, event_id)

    # Copy event information into deleted history
    deleted_event = DeletedEvent(
        original_event_id=event.id,
        title=event.title,
        description=event.description,
        event_date=event.event_date,
        event_type=event.event_type,
        deleted_at=datetime.utcnow()
    )

    db.session.add(deleted_event)

    # Remove original event
    db.session.delete(event)

    db.session.commit()

    flash("Event deleted and history saved successfully!", "success")

    return redirect(url_for("events.view_events"))


@event_bp.route("/events/history")
def deleted_history():

    deleted_events = DeletedEvent.query.order_by(
        DeletedEvent.deleted_at.desc()
    ).all()

    return render_template(
        "deleted_history.html",
        deleted_events=deleted_events
    )

# Permanently delete a history record
@event_bp.route(
    "/events/history/delete/<int:history_id>",
    methods=["POST"]
)
def permanently_delete_history(history_id):

    deleted_event = db.get_or_404(DeletedEvent, history_id)

    db.session.delete(deleted_event)
    db.session.commit()

    flash("Deleted history record permanently removed!", "success")

    return redirect(url_for("events.deleted_history"))
