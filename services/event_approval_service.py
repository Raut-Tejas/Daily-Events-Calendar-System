
from services.event_database_service import get_db_connection
from services.recurring_event_service import create_one_time_event


def get_pending_events():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                event_name,
                event_date,
                category,
                description,
                region,
                is_public_holiday,
                source,
                source_url,
                verification_status,
                imported_at
            FROM imported_events
            WHERE verification_status = 'pending'
            ORDER BY event_date ASC
        """)

        events = cursor.fetchall()
        cursor.close()

        return events

    finally:
        connection.close()


def approve_imported_event(event_id):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                event_name,
                event_date,
                category,
                description,
                verification_status,
                region,
                source
            FROM imported_events
            WHERE id = %s
            FOR UPDATE
        """, (event_id,))

        event = cursor.fetchone()

        if not event:
            raise ValueError("Imported event not found.")

        (
            event_name,
            event_date,
            category,
            description,
            status,
            region,
            source
        ) = event

        if status != "pending":
            raise ValueError(
                "This event has already been reviewed."
            )

        cursor.execute("""
            INSERT INTO events (
                title,
                description,
                event_date,
                event_type
            )
            VALUES (%s, %s, %s, %s)
        """, (
            event_name,
            description,
            event_date,
            category or "General"
        ))

        create_one_time_event(
            cursor=cursor,
            event_name=event_name,
            event_date=event_date,
            category=category or "General",
            description=description,
            region=region or "India",
            source=source or "Calendarific"
        )

        cursor.execute("""
            UPDATE imported_events
            SET verification_status = 'verified',
                reviewed_at = CURRENT_TIMESTAMP
            WHERE id = %s
              AND verification_status = 'pending'
        """, (event_id,))

        if cursor.rowcount != 1:
            raise ValueError(
                "Unable to update imported event status."
            )

        connection.commit()

        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def reject_imported_event(event_id):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE imported_events
            SET verification_status = 'rejected',
                reviewed_at = CURRENT_TIMESTAMP
            WHERE id = %s
              AND verification_status = 'pending'
            RETURNING id
        """, (event_id,))

        rejected_event = cursor.fetchone()

        if not rejected_event:
            raise ValueError(
                "Event not found or already reviewed."
            )

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
