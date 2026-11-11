
from getpass import getpass

from sqlalchemy import func, select
from werkzeug.security import generate_password_hash

from app import app
from models import Role, User, UserRole
from models.extensions import db


def create_admin():
    with app.app_context():
        # Find the admin role
        admin_role = db.session.scalar(
            select(Role).where(Role.code == "admin")
        )

        if admin_role is None:
            print("Admin role not found. Run seed.py first.")
            return

        # Ask for account information
        username = input("Admin username: ").strip()
        email = input("Admin email: ").strip()
        display_name = input("Display name: ").strip()

        if not username or not email or not display_name:
            print("All fields are required.")
            return

        # Check for an existing username or email
        existing_user = db.session.scalar(
            select(User).where(
                (func.lower(User.username) == username.lower())
                | (func.lower(User.email) == email.lower())
            )
        )

        if existing_user is not None:
            print("Username or email already exists.")
            return

        # Ask for password without displaying it
        password = getpass("Admin password: ")
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            print("Passwords do not match.")
            return

        if len(password) < 12:
            print("Password must contain at least 12 characters.")
            return

        # Create admin user
        admin = User(
            username=username,
            email=email,
            display_name=display_name,
            password_hash=generate_password_hash(password),
            preferred_language="en",
            is_active=True,
        )

        try:
            db.session.add(admin)
            db.session.flush()

            # Assign the existing admin role
            admin_user_role = UserRole(
                user_id=admin.id,
                role_id=admin_role.id,
            )

            db.session.add(admin_user_role)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        print("Admin account created successfully!")


if __name__ == "__main__":
    create_admin()
