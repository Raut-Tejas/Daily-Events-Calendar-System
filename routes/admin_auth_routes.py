from services.notification_admin_service import (
    get_notification_statistics
)

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from sqlalchemy import text

from extensions import db
from database.models import Event, DeletedEvent
from services.admin_auth_service import authenticate_admin


admin_auth_bp = Blueprint(
    "admin_auth",
    __name__,
    url_prefix="/admin"
)


@admin_auth_bp.route("/login", methods=["GET", "POST"])
def admin_login():

    if current_user.is_authenticated:
        return redirect(url_for("admin_auth.admin_dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = authenticate_admin(username, password)

        if admin:
            login_user(admin)

            flash("Welcome back, Admin!", "success")

            next_page = request.args.get("next")

            if (
                next_page
                and next_page.startswith("/")
                and not next_page.startswith("//")
            ):
                return redirect(next_page)

            return redirect(url_for("admin_auth.admin_dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("admin/login.html")


@admin_auth_bp.route("/dashboard")
@login_required
def admin_dashboard():

    total_events = Event.query.count()
    deleted_events = DeletedEvent.query.count()

    imported_stats = db.session.execute(
        text("""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (
                    WHERE verification_status = 'pending'
                ) AS pending,
                COUNT(*) FILTER (
                    WHERE verification_status = 'verified'
                ) AS approved,
                COUNT(*) FILTER (
                    WHERE verification_status = 'rejected'
                ) AS rejected
            FROM imported_events
        """)
    ).mappings().one()

    stats = {
        "total_events": total_events,
        "deleted_events": deleted_events,
        "imported_events": imported_stats["total"],
        "pending_events": imported_stats["pending"],
        "approved_events": imported_stats["approved"],
        "rejected_events": imported_stats["rejected"]
    }
    notification_stats = get_notification_statistics()
    return render_template(
    "admin/dashboard.html",
    stats=stats,
    notification_stats=notification_stats
)


@admin_auth_bp.route("/logout", methods=["POST"])
@login_required
def admin_logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("admin_auth.admin_login"))
