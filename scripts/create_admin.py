
import getpass
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from app import app
from services.admin_auth_service import create_admin


def main():

    print("\nDAYMARK - ADMIN ACCOUNT CREATION\n")

    username = input("Enter Admin Username: ").strip()
    email = input("Enter Admin Email: ").strip()

    password = getpass.getpass("Enter Admin Password: ")
    confirm_password = getpass.getpass("Confirm Admin Password: ")

    if password != confirm_password:
        print("\nERROR: Passwords do not match.")
        return

    try:
        with app.app_context():

            admin = create_admin(
                username=username,
                email=email,
                password=password
            )

            print("\nAdmin account created successfully!")
            print("Admin ID:", admin.id)
            print("Username:", admin.username)
            print("Email:", admin.email)

    except ValueError as error:
        print("\nERROR:", error)

    except Exception as error:
        print("\nDatabase error:", str(error))


if __name__ == "__main__":
    main()
