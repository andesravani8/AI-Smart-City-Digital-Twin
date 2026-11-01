from datetime import datetime
from backend.services.analytics_service import analytics_service


class AssistantService:
    def answer(self, message):
        text = (message or "").strip().lower()
        summary = analytics_service.get_dashboard_summary()
        if "traffic" in text:
            return "Traffic is monitored through the traffic ML module. Once the trained model is loaded, this assistant can explain the predicted volume and congestion level."
        if "air" in text or "aqi" in text:
            return "Air quality insights come from the air-quality ML module. The dashboard can surface AQI trends and identify unhealthy conditions."
        if "energy" in text:
            return "Energy demand is tracked from the energy dataset and can be forecast for planning peak-load periods."
        if "accident" in text or "risk" in text:
            return "Accident analytics can highlight high-risk zones and support preventive action by city operators."
        if "weather" in text:
            return "Weather data can be used to explain how temperature, rain and wind may affect other city systems."
        available = [k for k,v in summary.items() if v.get("available")]
        if available:
            return f"I can explain traffic, air quality, accidents, energy and weather. Currently available dataset modules: {', '.join(available)}."
        return "I can help with traffic, air quality, accidents, energy, weather, alerts and what-if city simulations."


assistant_service = AssistantService()
