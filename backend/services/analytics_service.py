import os
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATA_DIR = os.path.join(BASE_DIR, "data")


class AnalyticsService:
    """Reads the project's existing ML datasets for the Reports page.

    The ML model files and prediction routes are not modified by this service.
    """

    DATASET_FILES = {
        "traffic": "traffic.csv",
        "air_quality": "air_quality.csv.csv",
        "accidents": "Road.csv.csv",
        "energy": "Energy.csv.csv",
        "weather": "weather.csv.csv",
    }

    def load_dataset(self, module_name):
        filename = self.DATASET_FILES.get(module_name)
        if not filename:
            return None

        path = os.path.join(DATA_DIR, filename)
        if not os.path.isfile(path):
            return None

        try:
            return pd.read_csv(path)
        except Exception as exc:
            print(f"Error loading {module_name} dataset: {exc}")
            return None

    def get_module_summary(self, module_name):
        df = self.load_dataset(module_name)

        if df is None:
            filename = self.DATASET_FILES.get(module_name, "unknown")
            return {
                "available": False,
                "message": f"Dataset not found: {filename}",
                "file": filename,
            }

        return {
            "available": True,
            "records": int(len(df)),
            "columns": int(len(df.columns)),
            "features": list(df.columns),
            "file": self.DATASET_FILES[module_name],
        }

    def get_dashboard_summary(self):
        modules = [
            "traffic",
            "air_quality",
            "accidents",
            "energy",
            "weather",
        ]

        return {
            module: self.get_module_summary(module)
            for module in modules
        }


analytics_service = AnalyticsService()
