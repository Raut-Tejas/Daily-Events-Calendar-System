
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db
from database.models import Admin



# 1. CREATE ADMIN ACCOUNT


def create_admin(username, email, password):

    username = username.strip()
    email = email.strip().lower()

    if not username or not email or not password:
        raise ValueError("All fields are required.")

    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    existing_admin = Admin.query.filter(
        (db.func.lower(Admin.username) == username.lower()) |
        (db.func.lower(Admin.email) == email)
    ).first()

    if existing_admin:
        raise ValueError(
            "Username or email already exists."
        )

    password_hash = generate_password_hash(password)

    new_admin = Admin(
        username=username,
        email=email,
        password_hash=password_hash
    )

    try:
        db.session.add(new_admin)
        db.session.commit()

        return new_admin

    except Exception:
        db.session.rollback()
        raise



# 2. AUTHENTICATE ADMIN


def authenticate_admin(username, password):

    if not username or not password:
        return None

    admin = Admin.query.filter(
        db.func.lower(Admin.username) == username.strip().lower()
    ).first()

    if admin and check_password_hash(
        admin.password_hash,
        password
    ):
        return admin

    return None



# 3. GET ADMIN BY ID


def get_admin_by_id(admin_id):

    return db.session.get(Admin, admin_id)
