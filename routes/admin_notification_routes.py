
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from services.notification_admin_service import (
    get_notification_history,
    get_notification_statistics
)

admin_notification_bp = Blueprint(
    "admin_notification",
    __name__,
    url_prefix="/admin"
)



@admin_notification_bp.route("/notifications")
@login_required
def notification_dashboard():

    try:
        notifications = get_notification_history()
        stats = get_notification_statistics()

        return render_template(
            "admin/notifications.html",
            notifications=notifications,
            stats=stats
        )

    except Exception as error:
        import traceback

        traceback.print_exc()

        flash(
            f"Notification error: {str(error)}",
            "error"
        )

        return redirect(
            url_for("admin_auth.admin_dashboard")
        )
