
from psycopg2.extras import Json


def create_one_time_event(
    cursor,
    event_name,
    event_date,
    category,
    description,
    region,
    source
):
    if not event_name or not event_date:
        raise ValueError("Event name and date are required.")

    occurrence_year = event_date.year
    event_date_string = event_date.isoformat()

    cursor.execute("""
        SELECT id
        FROM recurring_event_templates
        WHERE event_name = %s
          AND category = %s
          AND region = %s
          AND recurrence_type = 'one_time'
          AND recurrence_rule->>'event_date' = %s
        LIMIT 1
    """, (
        event_name,
        category,
        region,
        event_date_string
    ))

    existing_template = cursor.fetchone()

    if existing_template:
        template_id = existing_template[0]

    else:
        recurrence_rule = {
            "event_date": event_date_string
        }

        cursor.execute("""
            INSERT INTO recurring_event_templates (
                event_name,
                category,
                description,
                recurrence_type,
                recurrence_rule,
                region,
                notification_enabled
            )
            VALUES (%s, %s, %s, 'one_time', %s, %s, TRUE)
            RETURNING id
        """, (
            event_name,
            category,
            description,
            Json(recurrence_rule),
            region
        ))

        template_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO event_occurrences (
            recurring_event_id,
            occurrence_year,
            event_date,
            calculation_status,
            source
        )
        VALUES (%s, %s, %s, 'verified', %s)
        ON CONFLICT (
            recurring_event_id,
            occurrence_year
        )
        DO NOTHING
    """, (
        template_id,
        occurrence_year,
        event_date,
        source
    ))

    return template_id
