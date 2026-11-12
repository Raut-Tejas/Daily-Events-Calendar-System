
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from services.event_approval_service import (
    get_pending_events,
    approve_imported_event,
    reject_imported_event
)

admin_approval_bp = Blueprint(
    "admin_approval",
    __name__,
    url_prefix="/admin"
)


@admin_approval_bp.route("/imported-events")
@login_required
def imported_events():
    try:
        events = get_pending_events()

        return render_template(
            "admin/imported_events.html",
            events=events
        )

    except Exception:
        flash("Unable to load imported events.", "error")
        return redirect(url_for("admin_auth.admin_dashboard"))


@admin_approval_bp.route(
    "/approve-event/<int:event_id>",
    methods=["POST"]
)
@login_required
def approve_event(event_id):
    try:
        approve_imported_event(event_id)
        flash("Event approved and published successfully!", "success")

    except ValueError as error:
        flash(str(error), "error")

    except Exception:
        flash("Unable to approve this event.", "error")

    return redirect(url_for("admin_approval.imported_events"))


@admin_approval_bp.route(
    "/reject-event/<int:event_id>",
    methods=["POST"]
)
@login_required
def reject_event(event_id):
    try:
        reject_imported_event(event_id)
        flash("Event rejected successfully.", "success")

    except ValueError as error:
        flash(str(error), "error")

    except Exception:
        flash("Unable to reject this event.", "error")

    return redirect(url_for("admin_approval.imported_events"))
