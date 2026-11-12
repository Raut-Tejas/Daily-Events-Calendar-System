
import os
import psycopg2

from pathlib import Path
from dotenv import load_dotenv


 # 1. LOAD ENVIRONMENT VARIABLES
 
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


 # 2. DATABASE CONNECTION
 
def get_db_connection():

    try:

        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        return connection

    except psycopg2.Error as error:

        raise RuntimeError(
            "PostgreSQL connection failed: "
            + str(error).splitlines()[0]
        )


 # 3. SAVE IMPORTED EVENTS
 
def save_imported_events(events):

    connection = get_db_connection()

    inserted_count = 0
    duplicate_count = 0

    try:

        with connection.cursor() as cursor:

            for event in events:

                query = """
                    INSERT INTO imported_events
                    (
                        event_name,
                        event_date,
                        category,
                        description,
                        region,
                        is_public_holiday,
                        source,
                        source_url,
                        verification_status
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, 'pending'
                    )
                    ON CONFLICT (
                        event_name,
                        event_date,
                        region,
                        source
                    )
                    DO NOTHING
                    RETURNING id;
                """

                cursor.execute(
                    query,
                    (
                        event["event_name"],
                        event["event_date"],
                        event["category"],
                        event.get("description", ""),
                        event.get("region", "India"),
                        event.get("is_public_holiday", False),
                        event.get("source", "Calendarific"),
                        event.get("source_url", "")
                    )
                )

                if cursor.fetchone():
                    inserted_count += 1
                else:
                    duplicate_count += 1

        connection.commit()

        return {
            "success": True,
            "inserted": inserted_count,
            "duplicates": duplicate_count,
            "total": len(events)
        }

    except Exception:

        connection.rollback()
        raise

    finally:

        connection.close()


 # 4. FETCH IMPORTED EVENTS
 
def get_imported_events():

    connection = get_db_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    id,
                    event_name,
                    event_date,
                    category,
                    region,
                    verification_status,
                    source
                FROM imported_events
                ORDER BY event_date;
            """)

            columns = [
                description[0]
                for description in cursor.description
            ]

            rows = cursor.fetchall()

            return [
                dict(zip(columns, row))
                for row in rows
            ]

    finally:

        connection.close()
