
from werkzeug.security import generate_password_hash, check_password_hash

from src.database import (
    create_user,
    get_user_by_email
)


def register_user(full_name, email, password, role):
    """Register a candidate or employer."""

    full_name = full_name.strip()
    email = email.strip().lower()

    if not full_name:
        raise ValueError("Full name is required.")

    if not email or "@" not in email:
        raise ValueError("Enter a valid email address.")

    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    if role not in ("candidate", "employer"):
        raise ValueError("Invalid account type.")

    if get_user_by_email(email):
        raise ValueError("An account with this email already exists.")

    password_hash = generate_password_hash(password)

    return create_user(
        full_name=full_name,
        email=email,
        password_hash=password_hash,
        role=role
    )


def authenticate_user(email, password):
    """Authenticate a user using their email and password."""

    user = get_user_by_email(email)

    if not user:
        return None

    if not check_password_hash(user["password_hash"], password):
        return None

    return user
