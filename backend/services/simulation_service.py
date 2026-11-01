# Service logic
from datetime import datetime


class SimulationService:

    def __init__(self):

        self.scenarios = []

    def calculate_impact(
        self,
        traffic_change,
        air_quality_change,
        energy_change
    ):

        # Base values
        traffic_score = 50
        air_quality_score = 50
        energy_score = 50

        # Apply user changes
        traffic_score += traffic_change
        air_quality_score += air_quality_change
        energy_score += energy_change

        # Keep values between 0 and 100
        traffic_score = max(0, min(100, traffic_score))
        air_quality_score = max(0, min(100, air_quality_score))
        energy_score = max(0, min(100, energy_score))

        # Overall city impact
        overall_score = (
            traffic_score +
            air_quality_score +
            energy_score
        ) / 3

        if overall_score >= 75:
            city_status = "Critical"
        elif overall_score >= 55:
            city_status = "Warning"
        else:
            city_status = "Stable"

        return {
            "traffic_impact": round(traffic_score, 2),
            "air_quality_impact": round(air_quality_score, 2),
            "energy_impact": round(energy_score, 2),
            "overall_impact": round(overall_score, 2),
            "city_status": city_status
        }

    def run_simulation(self, data):

        traffic_change = float(
            data.get("traffic_change", 0)
        )

        air_quality_change = float(
            data.get("air_quality_change", 0)
        )

        energy_change = float(
            data.get("energy_change", 0)
        )

        result = self.calculate_impact(
            traffic_change,
            air_quality_change,
            energy_change
        )

        scenario = {
            "id": len(self.scenarios) + 1,
            "inputs": {
                "traffic_change": traffic_change,
                "air_quality_change": air_quality_change,
                "energy_change": energy_change
            },
            "result": result,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        self.scenarios.insert(0, scenario)

        return scenario

    def get_history(self):

        return self.scenarios


simulation_service = SimulationService()