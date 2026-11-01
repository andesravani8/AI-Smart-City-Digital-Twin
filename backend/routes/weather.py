from flask import Blueprint, jsonify, request, render_template
from backend.database import database
from utils.model_loader import model_loader
import pandas as pd


weather_bp = Blueprint("weather", __name__)
@weather_bp.route("/")
def weather_page():
    return render_template("modules/weather.html")

@weather_bp.route("/predict", methods=["POST"])
def predict_weather():

    data = request.get_json(silent=True) or {}

    try:

        # --------------------------------------------------
        # GET LOADED MODEL
        # --------------------------------------------------

        model = model_loader.models.get("weather")
        preprocessor = model_loader.preprocessors.get("weather")

        if model is None or preprocessor is None:

            return jsonify({
                "success": False,
                "message": "Weather ML model or preprocessor is not loaded"
            }), 500


        # --------------------------------------------------
        # GET INPUT VALUES
        # --------------------------------------------------

        pressure = float(data.get("pressure"))
        tpot = float(data.get("tpot"))
        tdew = float(data.get("tdew"))
        humidity = float(data.get("humidity"))
        vpmax = float(data.get("vpmax"))
        vpact = float(data.get("vpact"))
        vpdef = float(data.get("vpdef"))
        specific_humidity = float(data.get("specific_humidity"))
        h2oc = float(data.get("h2oc"))
        density = float(data.get("density"))
        windspeed = float(data.get("windspeed"))
        max_windspeed = float(data.get("max_windspeed"))
        wind_direction = float(data.get("wind_direction"))

        year = int(data.get("year"))
        month = int(data.get("month"))
        day = int(data.get("day"))
        hour = int(data.get("hour"))
        day_of_week = int(data.get("day_of_week"))


        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        if not 0 <= humidity <= 100:

            return jsonify({
                "success": False,
                "message": "Humidity must be between 0 and 100"
            }), 400


        if not 0 <= hour <= 23:

            return jsonify({
                "success": False,
                "message": "Hour must be between 0 and 23"
            }), 400


        if not 1 <= month <= 12:

            return jsonify({
                "success": False,
                "message": "Month must be between 1 and 12"
            }), 400


        if not 1 <= day <= 31:

            return jsonify({
                "success": False,
                "message": "Day must be between 1 and 31"
            }), 400


        # --------------------------------------------------
        # FEATURE NAMES FROM TRAINED PREPROCESSOR
        # --------------------------------------------------

        expected_features = list(
            preprocessor.feature_names_in_
        )


        # --------------------------------------------------
        # CREATE INPUT ROW
        # --------------------------------------------------

        values = {

            "p (mbar)": pressure,

            "Tpot (K)": tpot,

            "Tdew (degC)": tdew,

            "rh (%)": humidity,

            "VPmax (mbar)": vpmax,

            "VPact (mbar)": vpact,

            "VPdef (mbar)": vpdef,

            "sh (g/kg)": specific_humidity,

            "H2OC (mmol/mol)": h2oc,

            "rho (g/m**3)": density,

            "wv (m/s)": windspeed,

            "max. wv (m/s)": max_windspeed,

            "wd (deg)": wind_direction,

            "Year": year,

            "Month": month,

            "Day": day,

            "Hour": hour,

            "DayOfWeek": day_of_week

        }


        # --------------------------------------------------
        # MATCH TRAINING FEATURE ORDER
        # --------------------------------------------------

        row = {}

        for feature in expected_features:

            row[feature] = values.get(
                feature,
                None
            )


        input_df = pd.DataFrame(
            [row],
            columns=expected_features
        )


        # --------------------------------------------------
        # PREPROCESS
        # --------------------------------------------------

        transformed_data = preprocessor.transform(
            input_df
        )


        # --------------------------------------------------
        # ML PREDICTION
        # --------------------------------------------------

        prediction = float(
            model.predict(transformed_data)[0]
        )


        prediction = round(
            prediction,
            2
        )


        # --------------------------------------------------
        # TEMPERATURE LEVEL
        # --------------------------------------------------

        if prediction < 15:

            temperature_level = "Cold"

        elif prediction < 25:

            temperature_level = "Cool"

        elif prediction < 32:

            temperature_level = "Moderate"

        elif prediction < 38:

            temperature_level = "Hot"

        else:

            temperature_level = "Very Hot"


        # --------------------------------------------------
        # RISK LEVEL
        # --------------------------------------------------

        if prediction < 25:

            risk_level = "Low"

        elif prediction < 32:

            risk_level = "Medium"

        elif prediction < 38:

            risk_level = "High"

        else:

            risk_level = "Critical"


        # --------------------------------------------------
        # SAVE PREDICTION TO DATABASE
        # --------------------------------------------------

        connection = database.get_connection()

        if connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO predictions
                (module, prediction_value, risk_level, model_name)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    "weather",
                    str(prediction),
                    risk_level,
                    "Weather Temperature ML Model"
                )
            )

            connection.commit()

            cursor.close()
            connection.close()


        # --------------------------------------------------
        # RESPONSE
        # --------------------------------------------------

        return jsonify({

            "success": True,

            "module": "Weather",

            "prediction": {

                "temperature": prediction,

                "temperature_level": temperature_level,

                "risk_level": risk_level

            },

            "input": values,

            "prediction_type": "ML",

            "model": "Weather Temperature ML Model",

            "message":
                "Temperature predicted successfully"

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "message":
                "Weather ML prediction failed",

            "error": str(e)

        }), 500