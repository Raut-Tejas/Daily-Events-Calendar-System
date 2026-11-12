
from sqlalchemy import text
from extensions import db


def get_notification_history():
    query = text("""
        SELECT
            nl.id,
            nl.user_id,
            nl.reminder_type,
            nl.sent_at,
            eo.event_date,
            eo.occurrence_year,
            eo.calculation_status,
            ret.event_name,
            ret.category,
            ret.region
        FROM notification_logs nl
        JOIN event_occurrences eo
            ON nl.occurrence_id = eo.id
        JOIN recurring_event_templates ret
            ON eo.recurring_event_id = ret.id
        ORDER BY nl.sent_at DESC NULLS LAST, nl.id DESC
    """)

    result = db.session.execute(query)

    return result.mappings().all()


def get_notification_statistics():
    query = text("""
        SELECT
            COUNT(*) AS total_notifications,
            COUNT(DISTINCT user_id) AS total_users,
            COUNT(DISTINCT occurrence_id) AS notified_occurrences
        FROM notification_logs
    """)

    result = db.session.execute(query)

    return result.mappings().one()
