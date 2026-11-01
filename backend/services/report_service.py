from datetime import datetime
from backend.services.analytics_service import analytics_service


class ReportService:
    def summary(self):
        return {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modules": analytics_service.get_dashboard_summary(),
        }


report_service = ReportService()
