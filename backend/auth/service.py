import os
from werkzeug.security import check_password_hash, generate_password_hash
from backend.database import database


class AuthService:
    """Small authentication service used only by the login layer."""

    def ensure_default_admin(self):
        """Create the local demo admin if the users table is empty for that email."""
        email = os.getenv("ADMIN_EMAIL", "admin@smartcity.local").strip().lower()
        password = os.getenv("ADMIN_PASSWORD", "Admin@123")
        name = os.getenv("ADMIN_NAME", "Smart City Administrator")

        connection = database.get_connection()
        if not connection:
            print("Auth setup skipped: database unavailable.")
            return False

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE email = %s LIMIT 1", (email,))
            existing = cursor.fetchone()

            if not existing:
                cursor.execute(
                    """
                    INSERT INTO users (name, email, password_hash, role)
                    VALUES (%s, %s, %s, 'admin')
                    """,
                    (name, email, generate_password_hash(password))
                )
                connection.commit()
                print(f"Default admin created: {email}")
            return True
        except Exception as exc:
            connection.rollback()
            print("Auth setup error:", exc)
            return False
        finally:
            if cursor:
                cursor.close()
            connection.close()

    def authenticate(self, email, password):
        email = (email or "").strip().lower()
        if not email or not password:
            return None

        connection = database.get_connection()
        if not connection:
            return None

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, name, email, password_hash, role
                FROM users
                WHERE email = %s
                LIMIT 1
                """,
                (email,)
            )
            user = cursor.fetchone()

            if not user or not check_password_hash(user["password_hash"], password):
                return None

            user.pop("password_hash", None)
            return user
        except Exception as exc:
            print("Authentication error:", exc)
            return None
        finally:
            if cursor:
                cursor.close()
            connection.close()


    def get_user(self, user_id):
        connection = database.get_connection()
        if not connection:
            return None

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, name, email, role FROM users WHERE id = %s LIMIT 1",
                (user_id,)
            )
            return cursor.fetchone()
        except Exception as exc:
            print("User lookup error:", exc)
            return None
        finally:
            if cursor:
                cursor.close()
            connection.close()


auth_service = AuthService()
