from flask import Blueprint, jsonify, request
from backend.database import database
from utils.model_loader import model_loader
import pandas as pd
import joblib


air_quality_bp = Blueprint("air_quality", __name__)


@air_quality_bp.route("/predict", methods=["POST"])
def predict_air_quality():

    data = request.get_json(silent=True) or {}

    try:

        # ====================================================
        # GET ML MODEL
        # ====================================================

        air_quality_model = model_loader.models.get("air_quality")
        air_quality_preprocessor = model_loader.preprocessors.get(
            "air_quality"
        )

        if air_quality_model is None:
            return jsonify({
                "success": False,
                "message": "Air Quality ML model is not loaded"
            }), 500

        if air_quality_preprocessor is None:
            return jsonify({
                "success": False,
                "message": "Air Quality ML preprocessor is not loaded"
            }), 500


        # ====================================================
        # INPUT VALIDATION
        # ====================================================

        required_fields = [
            "city",
            "pm25",
            "pm10",
            "no",
            "no2",
            "nox",
            "nh3",
            "co",
            "so2",
            "o3",
            "benzene",
            "toluene",
            "xylene",
            "year",
            "month",
            "day"
        ]


        missing_fields = [
            field
            for field in required_fields
            if field not in data
        ]


        if missing_fields:

            return jsonify({
                "success": False,
                "message": "Missing required fields",
                "missing_fields": missing_fields
            }), 400


        # ====================================================
        # CREATE INPUT DATAFRAME
        # ====================================================

        input_data = pd.DataFrame([{

            "City": data["city"],

            "PM2.5": float(data["pm25"]),

            "PM10": float(data["pm10"]),

            "NO": float(data["no"]),

            "NO2": float(data["no2"]),

            "NOx": float(data["nox"]),

            "NH3": float(data["nh3"]),

            "CO": float(data["co"]),

            "SO2": float(data["so2"]),

            "O3": float(data["o3"]),

            "Benzene": float(data["benzene"]),

            "Toluene": float(data["toluene"]),

            "Xylene": float(data["xylene"]),

            "Year": int(data["year"]),

            "Month": int(data["month"]),

            "Day": int(data["day"])

        }])


        # ====================================================
        # PREPROCESS INPUT
        # ====================================================

        processed_data = air_quality_preprocessor.transform(
            input_data
        )


        # ====================================================
        # ML PREDICTION
        # ====================================================

        predicted_aqi = air_quality_model.predict(
            processed_data
        )[0]


        predicted_aqi = float(predicted_aqi)


        # AQI cannot be negative
        predicted_aqi = max(0, predicted_aqi)


        # ====================================================
        # AQI CATEGORY
        # ====================================================

        if predicted_aqi <= 50:

            category = "Good"
            risk = "Low"

        elif predicted_aqi <= 100:

            category = "Satisfactory"
            risk = "Low"

        elif predicted_aqi <= 200:

            category = "Moderate"
            risk = "Medium"

        elif predicted_aqi <= 300:

            category = "Poor"
            risk = "High"

        elif predicted_aqi <= 400:

            category = "Very Poor"
            risk = "High"

        else:

            category = "Severe"
            risk = "Critical"


        # ====================================================
        # SAVE PREDICTION TO DATABASE
        # ====================================================

        connection = database.get_connection()

        if connection:

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO predictions
                (
                    module,
                    prediction_value,
                    risk_level,
                    model_name
                )
                VALUES (%s, %s, %s, %s)
            """, (

                "air_quality",

                predicted_aqi,

                risk,

                "Air Quality ML Model"

            ))

            connection.commit()

            cursor.close()
            connection.close()


        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "success": True,

            "module": "air_quality",

            "input": data,

            "prediction": {

                "aqi": round(
                    predicted_aqi,
                    2
                ),

                "category": category,

                "risk_level": risk

            },

            "model": "Air Quality ML Model",

            "prediction_type": "ML",

            "message":
                "Air quality ML prediction generated successfully"

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "message":
                "Air quality ML prediction failed",

            "error": str(e)

        }), 500