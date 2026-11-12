
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from services.event_database_service import get_db_connection
from services.recurring_event_service import create_one_time_event


def backfill_missing_occurrences():

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                ie.event_name,
                ie.event_date,
                ie.category,
                ie.description,
                ie.region,
                ie.source
            FROM imported_events ie
            WHERE ie.verification_status = 'verified'
            AND NOT EXISTS (
                SELECT 1
                FROM recurring_event_templates ret
                JOIN event_occurrences eo
                    ON eo.recurring_event_id = ret.id
                WHERE ret.event_name = ie.event_name
                  AND eo.event_date = ie.event_date
            )
            ORDER BY ie.event_date ASC
        """)

        missing_events = cursor.fetchall()

        if not missing_events:
            print("No missing occurrences found.")
            return

        print(
            f"Found {len(missing_events)} missing occurrences."
        )

        for event in missing_events:

            (
                event_name,
                event_date,
                category,
                description,
                region,
                source
            ) = event

            create_one_time_event(
                cursor=cursor,
                event_name=event_name,
                event_date=event_date,
                category=category or "General",
                description=description,
                region=region or "India",
                source=source or "Calendarific"
            )

            print(
                f"Created occurrence: {event_name}"
            )

        connection.commit()

        print("\nBackfill completed successfully!")

    except Exception as error:
        connection.rollback()
        print("\nBackfill failed:", error)
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    backfill_missing_occurrences()
