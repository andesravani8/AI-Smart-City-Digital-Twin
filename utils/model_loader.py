import os
import joblib


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "ml", "models")


class ModelLoader:

    def __init__(self):
        self.models = {}
        self.preprocessors = {}
        self.errors = {}

    def _load(self, path, key, target):

        if not os.path.exists(path):
            self.errors[key] = "File not found"
            return None

        if os.path.getsize(path) == 0:
            self.errors[key] = "File is empty"
            return None

        try:
            obj = joblib.load(path)
            target[key] = obj

            print(f"Loaded: {key}")

            return obj

        except Exception as e:
            self.errors[key] = str(e)
            print(f"Error loading {key}: {e}")

            return None

    def load_model(self, name):

        path = os.path.join(
            MODEL_DIR,
            f"{name}_model.joblib"
        )

        return self._load(
            path,
            name,
            self.models
        )

    def load_preprocessor(self, name):

        path = os.path.join(
            MODEL_DIR,
            f"{name}_preprocessor.joblib"
        )

        return self._load(
            path,
            name,
            self.preprocessors
        )

    def load_all(self):

        self.models.clear()
        self.preprocessors.clear()
        self.errors.clear()
        print("DEBUG BASE_DIR:", BASE_DIR)
        print("DEBUG MODEL_DIR:", MODEL_DIR)
        print("DEBUG MODEL_DIR EXISTS:", os.path.exists(MODEL_DIR))

        if os.path.exists(MODEL_DIR):
            print("DEBUG FILES:", os.listdir(MODEL_DIR))
        modules = [
            "traffic",
            "air_quality",
            "accident",
            "energy",
            "weather"
        ]

        for module in modules:

            self.load_model(module)
            self.load_preprocessor(module)

        print("\n========== MODEL STATUS ==========")
        print("Models:", list(self.models.keys()))
        print("Preprocessors:", list(self.preprocessors.keys()))
        print("Errors:", self.errors)
        print("==================================\n")

        return self.models, self.preprocessors

    def status(self):

        return {
            "loaded_models": sorted(
                self.models.keys()
            ),

            "loaded_preprocessors": sorted(
                self.preprocessors.keys()
            ),

            "errors": self.errors
        }


model_loader = ModelLoader()