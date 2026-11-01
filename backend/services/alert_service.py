from datetime import datetime
from backend.database import database


class AlertService:

    def create_alert(
        self,
        module,
        level,
        title,
        message,
        value=None,
        threshold=None
    ):

        connection = database.get_connection()

        if not connection:
            return None

        try:

            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                INSERT INTO alerts
                (
                    module,
                    title,
                    message,
                    severity,
                    value,
                    threshold,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, 'active')
            """, (
                module,
                title,
                message,
                level,
                value,
                threshold
            ))

            connection.commit()

            alert_id = cursor.lastrowid

            cursor.execute("""
                SELECT
                    id,
                    module,
                    title,
                    message,
                    severity,
                    value,
                    threshold,
                    status,
                    created_at
                FROM alerts
                WHERE id = %s
            """, (alert_id,))

            alert = cursor.fetchone()

            cursor.close()
            connection.close()

            return alert

        except Exception as e:

            connection.rollback()
            connection.close()

            print("Alert creation error:", e)

            return None


    def check_prediction(
        self,
        module,
        value,
        threshold,
        title,
        message
    ):

        if value >= threshold:

            return self.create_alert(
                module=module,
                level="critical",
                title=title,
                message=message,
                value=value,
                threshold=threshold
            )

        return None


    def get_alerts(self):

        connection = database.get_connection()

        if not connection:
            return []

        try:

            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id,
                    module,
                    title,
                    message,
                    severity,
                    value,
                    threshold,
                    status,
                    created_at
                FROM alerts
                ORDER BY created_at DESC
            """)

            alerts = cursor.fetchall()

            cursor.close()
            connection.close()

            return alerts

        except Exception as e:

            print("Get alerts error:", e)

            connection.close()

            return []


    def get_active_alerts(self):

        connection = database.get_connection()

        if not connection:
            return []

        try:

            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id,
                    module,
                    title,
                    message,
                    severity,
                    value,
                    threshold,
                    status,
                    created_at
                FROM alerts
                WHERE status = 'active'
                ORDER BY created_at DESC
            """)

            alerts = cursor.fetchall()

            cursor.close()
            connection.close()

            return alerts

        except Exception as e:

            print("Get active alerts error:", e)

            connection.close()

            return []


    def clear_alert(self, alert_id):

        connection = database.get_connection()

        if not connection:
            return False

        try:

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE alerts
                SET
                    status = 'resolved',
                    resolved_at = NOW()
                WHERE id = %s
            """, (alert_id,))

            connection.commit()

            updated = cursor.rowcount > 0

            cursor.close()
            connection.close()

            return updated

        except Exception as e:

            print("Resolve alert error:", e)

            connection.rollback()
            connection.close()

            return False


alert_service = AlertService()