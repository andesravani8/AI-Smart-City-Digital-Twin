import numpy as np
from utils.model_loader import model_loader


class PredictionService:
    def __init__(self):
        self.models = {}
        self.preprocessors = {}
        self.load_models()

    def load_models(self):
        self.models, self.preprocessors = model_loader.load_all()

    def predict(self, module_name, data):
        if module_name not in self.models:
            return {
                "success": False,
                "module": module_name,
                "message": "Trained model is not available. Add the .joblib model from Google Colab."
            }

        try:
            model = self.models[module_name]
            preprocessor = self.preprocessors.get(module_name)
            input_data = np.asarray(data, dtype=float).reshape(1, -1)

            if preprocessor is not None:
                input_data = preprocessor.transform(input_data)

            prediction = model.predict(input_data)[0]
            if isinstance(prediction, np.generic):
                prediction = prediction.item()

            return {
                "success": True,
                "module": module_name,
                "prediction": prediction,
            }
        except Exception as exc:
            return {"success": False, "module": module_name, "message": str(exc)}


prediction_service = PredictionService()
