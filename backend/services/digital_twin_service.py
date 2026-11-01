from datetime import datetime
from backend.database import database


class DigitalTwinService:

    def __init__(self):

        self.city = {
            "id": "smart-city-001",
            "name": "Smart City",
            "country": "India"
        }


    def ensure_demo_zones(self):

        connection = database.get_connection()

        if not connection:
            return False

        cursor = None
        try:
            cursor = connection.cursor()

            zones = [
                ("Z-CENTRAL", "Central Zone", "central", 16.5062, 80.6480, "normal"),
                ("Z-RESIDENTIAL", "Residential Zone", "residential", 16.5153, 80.6365, "normal"),
                ("Z-COMMERCIAL", "Commercial Zone", "commercial", 16.4998, 80.6608, "warning"),
                ("Z-DANGER", "Industrial Danger Zone", "industrial", 16.4922, 80.6755, "critical"),
            ]

            for zone in zones:
                cursor.execute(
                    """
                    INSERT INTO city_zones
                    (zone_code, zone_name, zone_type, latitude, longitude, status)
                    SELECT %s, %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1 FROM city_zones WHERE zone_code = %s
                    )
                    """,
                    zone + (zone[0],)
                )

            infrastructure = [
                ("Z-CENTRAL", "Central Traffic Junction", "traffic_junction", "operational", 16.5062, 80.6480),
                ("Z-RESIDENTIAL", "City Power Substation", "power", "operational", 16.5153, 80.6365),
                ("Z-COMMERCIAL", "Commercial Monitoring Hub", "monitoring", "operational", 16.4998, 80.6608),
                ("Z-DANGER", "Industrial Safety Sensor", "safety_sensor", "warning", 16.4922, 80.6755),
            ]

            for zone_code, name, asset_type, status, lat, lng in infrastructure:
                cursor.execute(
                    """
                    INSERT INTO infrastructure
                    (zone_id, name, type, status, latitude, longitude)
                    SELECT z.id, %s, %s, %s, %s, %s
                    FROM city_zones z
                    WHERE z.zone_code = %s
                      AND NOT EXISTS (SELECT 1 FROM infrastructure i WHERE i.name = %s)
                    """,
                    (name, asset_type, status, lat, lng, zone_code, name)
                )

            connection.commit()
            return True
        except Exception as exc:
            connection.rollback()
            print("Demo zone setup skipped:", exc)
            return False
        finally:
            if cursor:
                cursor.close()
            connection.close()

    def get_city(self):

        return {
            "city": self.city,
            "zones": self.get_zones(),
            "infrastructure": self.get_infrastructure(),
            "last_updated": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }


    def get_zones(self):

        connection = database.get_connection()

        if not connection:
            return []

        try:

            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id,
                    zone_code,
                    zone_name,
                    zone_type,
                    latitude,
                    longitude,
                    status
                FROM city_zones
                ORDER BY id
            """)

            zones = cursor.fetchall()

            cursor.close()
            connection.close()

            return zones

        except Exception as e:

            print("Zone loading error:", e)

            connection.close()

            return []


    def get_zone(self, zone_id):

        connection = database.get_connection()

        if not connection:
            return None

        try:

            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id,
                    zone_code,
                    zone_name,
                    zone_type,
                    latitude,
                    longitude,
                    status
                FROM city_zones
                WHERE id = %s
            """, (zone_id,))

            zone = cursor.fetchone()

            cursor.close()
            connection.close()

            return zone

        except Exception as e:

            print("Zone error:", e)

            connection.close()

            return None


    def get_infrastructure(self):

        connection = database.get_connection()

        if not connection:
            return []

        try:

            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id,
                    zone_id,
                    name,
                    type,
                    status,
                    latitude,
                    longitude
                FROM infrastructure
                ORDER BY id
            """)

            infrastructure = cursor.fetchall()

            cursor.close()
            connection.close()

            return infrastructure

        except Exception as e:

            print("Infrastructure error:", e)

            connection.close()

            return []


    def update_zone_status(self, zone_id, status):

        allowed_status = [
            "normal",
            "warning",
            "critical"
        ]

        if status not in allowed_status:
            return None

        connection = database.get_connection()

        if not connection:
            return None

        try:

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE city_zones
                SET status = %s
                WHERE id = %s
            """, (
                status,
                zone_id
            ))

            connection.commit()

            cursor.close()
            connection.close()

            return self.get_zone(zone_id)

        except Exception as e:

            print("Zone update error:", e)

            connection.rollback()
            connection.close()

            return None


digital_twin_service = DigitalTwinService()