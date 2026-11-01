from flask import Blueprint, jsonify, request
from backend.database import database
from utils.model_loader import model_loader
import pandas as pd

energy_bp = Blueprint("energy", __name__)


@energy_bp.route("/predict", methods=["POST"])
def predict_energy():

    data = request.get_json(silent=True) or {}

    try:
        # Get trained ML model
        model = model_loader.models.get("energy")
        preprocessor = model_loader.preprocessors.get("energy")

        if model is None or preprocessor is None:
            return jsonify({
                "success": False,
                "message": "Energy ML model or preprocessor is not loaded"
            }), 500

        # ------------------------------------------------
        # Get inputs
        # ------------------------------------------------

        month = int(data.get("month"))
        hour = int(data.get("hour"))
        day_of_week = int(data.get("day_of_week"))

        holiday = data.get("holiday")
        temperature = float(data.get("temperature"))
        humidity = float(data.get("humidity"))
        square_footage = float(data.get("square_footage"))
        occupancy = float(data.get("occupancy"))
        hvac_usage = data.get("hvac_usage")
        lighting_usage = data.get("lighting_usage")
        renewable_energy = float(data.get("renewable_energy"))

        # ------------------------------------------------
        # Convert categorical values
        # ------------------------------------------------

        if str(holiday).lower() in ["yes", "true", "1"]:
            holiday = "Yes"
        else:
            holiday = "No"

        # ------------------------------------------------
        # Create input dataframe
        # ------------------------------------------------

        expected_features = list(
            preprocessor.feature_names_in_
        )

        row = {}

        for feature in expected_features:
            row[feature] = None

        values = {
            "Month": month,
            "Hour": hour,
            "DayOfWeek": day_of_week,
            "Holiday": holiday,
            "Temperature": temperature,
            "Humidity": humidity,
            "SquareFootage": square_footage,
            "Occupancy": occupancy,
            "HVACUsage": hvac_usage,
            "LightingUsage": lighting_usage,
            "RenewableEnergy": renewable_energy
        }

        for feature in expected_features:

            if feature in values:
                row[feature] = values[feature]

        input_df = pd.DataFrame(
            [row],
            columns=expected_features
        )

        # ------------------------------------------------
        # Preprocess
        # ------------------------------------------------

        transformed = preprocessor.transform(
            input_df
        )

        # ------------------------------------------------
        # ML Prediction
        # ------------------------------------------------

        prediction = model.predict(
            transformed
        )[0]

        prediction = float(prediction)

        # ------------------------------------------------
        # Energy classification
        # ------------------------------------------------

        if prediction < 300:
            demand_level = "Low"

        elif prediction < 700:
            demand_level = "Moderate"

        elif prediction < 1000:
            demand_level = "High"

        else:
            demand_level = "Very High"

        # ------------------------------------------------
        # Risk level
        # ------------------------------------------------

        if prediction < 300:
            risk_level = "Low"

        elif prediction < 700:
            risk_level = "Medium"

        elif prediction < 1000:
            risk_level = "High"

        else:
            risk_level = "Critical"

        # ------------------------------------------------
        # Save prediction to database
        # ------------------------------------------------

        connection = database.get_connection()

        if connection:

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO predictions
                (module, prediction_value, risk_level, model_name)
                VALUES (%s, %s, %s, %s)
            """, (
                "energy",
                str(round(prediction, 2)),
                risk_level,
                "Energy Consumption ML Model"
            ))

            connection.commit()

            cursor.close()
            connection.close()

        # ------------------------------------------------
        # Response
        # ------------------------------------------------

        return jsonify({

            "success": True,

            "module": "Energy",

            "prediction": {
                "energy_consumption": round(
                    prediction,
                    2
                ),
                "demand_level": demand_level,
                "risk_level": risk_level
            },

            "input": values,

            "prediction_type": "ML",

            "model": "Energy Consumption ML Model",

            "message":
                "Energy consumption predicted successfully"
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message":
                "Energy ML prediction failed",

            "error": str(e)
        }), 500