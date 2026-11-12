
import os
import requests

from pathlib import Path
from dotenv import load_dotenv
from datetime import date


 # 1. ENVIRONMENT CONFIGURATION
 
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

CALENDARIFIC_API_KEY = os.getenv(
    "CALENDARIFIC_API_KEY", ""
).strip()

CALENDARIFIC_URL = (
    "https://calendarific.com/api/v2/holidays"
)


 # 2. VALIDATE API CONFIGURATION
 
def validate_api_key():

    if not CALENDARIFIC_API_KEY:
        raise ValueError(
            "Calendarific API key not found. "
            "Check your .env file."
        )


 # 3. MAP EVENT CATEGORIES
 
def get_event_category(event_types):

    types = [
        str(item).lower()
        for item in event_types
    ]

    if any("national" in item for item in types):
        return "National Holiday"

    if any("religious" in item for item in types):
        return "Religious Event"

    if any("local" in item for item in types):
        return "Cultural Event"

    return "Cultural Event"


 # 4. FETCH EVENTS FROM CALENDARIFIC
 
def import_calendarific_events(year):

    validate_api_key()

    if not isinstance(year, int) or not 1900 <= year <= 2100:
        raise ValueError("Please provide a valid year.")

    params = {
        "api_key": CALENDARIFIC_API_KEY,
        "country": "IN",
        "year": year
    }

    try:

        response = requests.get(
            CALENDARIFIC_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        meta = data.get("meta", {})

        if meta.get("code") != 200:
            raise RuntimeError(
                "Calendarific API error: "
                + str(meta.get("error_detail", "Unknown error"))
            )

        holidays = data.get(
            "response", {}
        ).get("holidays", [])

        imported_events = []

        for holiday in holidays:

            event_name = holiday.get("name")

            event_date = holiday.get(
                "date", {}
            ).get("iso", "")

            if not event_name or not event_date:
                continue

            # Keep only the date portion
            event_date = event_date[:10]

            # Validate date
            try:
                parsed_date = date.fromisoformat(event_date)
            except ValueError:
                continue

            if parsed_date.year != year:
                continue

            event_types = holiday.get("type", [])

            if isinstance(event_types, str):
                event_types = [event_types]

            category = get_event_category(event_types)

            is_public_holiday = any(
                "national" in str(item).lower()
                for item in event_types
            )

            imported_events.append({

                "event_name": event_name,

                "event_date": event_date,

                "category": category,

                "description": (
                    holiday.get("description") or ""
                ),

                "region": "India",

                "is_public_holiday": is_public_holiday,

                "source": "Calendarific",

                "source_url": holiday.get(
                    "canonical_url"
                ) or CALENDARIFIC_URL

            })

        return imported_events

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Calendarific request timed out."
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot connect to Calendarific. "
            "Check your internet connection."
        )

    except requests.exceptions.HTTPError as error:

        status = error.response.status_code

        if status == 401:
            raise RuntimeError(
                "Invalid Calendarific API key."
            )

        elif status == 403:
            raise RuntimeError(
                "Calendarific access forbidden."
            )

        elif status == 429:
            raise RuntimeError(
                "Calendarific API request limit reached."
            )

        else:
            raise RuntimeError(
                f"Calendarific HTTP error: {status}"
            )

    except requests.exceptions.RequestException:
        raise RuntimeError(
            "Calendarific network request failed."
        )


 # 5. REMOVE DUPLICATE EVENTS
 
def remove_duplicate_events(events):

    unique_events = {}

    for event in events:

        key = (
            event["event_name"].strip().lower(),
            event["event_date"],
            event["region"].strip().lower()
        )

        unique_events[key] = event

    return list(unique_events.values())


 # 6. MAIN EVENT IMPORT FUNCTION
 
def fetch_indian_events(year):

    print(f"Fetching Indian events for {year}...")

    events = import_calendarific_events(year)

    events = remove_duplicate_events(events)

    print(
        f"Successfully fetched {len(events)} events."
    )

    return events


 # 7. TEST SERVICE DIRECTLY
 
if __name__ == "__main__":

    try:

        year = 2027

        events = fetch_indian_events(year)

        print("\n========== IMPORTED EVENTS ==========\n")

        for event in events:

            print("Event:", event["event_name"])
            print("Date:", event["event_date"])
            print("Category:", event["category"])
            print("Description:", event["description"])
            print("Public Holiday:", event["is_public_holiday"])
            print("Source:", event["source"])

            print("------------------------------------")

        print("\nTotal Events:", len(events))

    except (RuntimeError, ValueError) as error:

        print("\nERROR:", error)
