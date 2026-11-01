from flask import Blueprint, jsonify, request
from backend.database import database
from utils.model_loader import model_loader
import joblib
import os
import pandas as pd


accidents_bp = Blueprint("accidents", __name__)


# =========================================================
# MODEL DIRECTORY
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

MODEL_DIR = os.path.join(BASE_DIR, "ml", "models")


# =========================================================
# LOAD LABEL ENCODER
# =========================================================

LABEL_ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "accident_label_encoder.joblib"
)

try:

    accident_label_encoder = joblib.load(
        LABEL_ENCODER_PATH
    )

    print("✅ Accident label encoder loaded successfully")
    print(
        "Encoder classes:",
        accident_label_encoder.classes_
    )

except Exception as e:

    accident_label_encoder = None

    print("❌ Accident label encoder failed to load")
    print("Path:", LABEL_ENCODER_PATH)
    print("Error:", e)


# =========================================================
# ACCIDENT PREDICTION
# =========================================================

@accidents_bp.route("/predict", methods=["POST"])
def predict_accident():

    data = request.get_json(silent=True) or {}

    try:

        # -------------------------------------------------
        # GET MODEL AND PREPROCESSOR
        # -------------------------------------------------

        model = model_loader.models.get("accident")
        preprocessor = model_loader.preprocessors.get("accident")

        if model is None or preprocessor is None:

            return jsonify({
                "success": False,
                "message":
                    "Accident ML model or preprocessor is not loaded"
            }), 500


        if accident_label_encoder is None:

            return jsonify({
                "success": False,
                "message":
                    "Accident label encoder is not loaded"
            }), 500


        # =================================================
        # 8 USER INPUTS
        # =================================================

        vehicles = int(
            data.get(
                "number_of_vehicles_involved",
                2
            )
        )

        vehicle_type = data.get(
            "type_of_vehicle",
            "Automobile"
        )

        collision = data.get(
            "type_of_collision",
            "Vehicle with vehicle collision"
        )

        road_surface = data.get(
            "road_surface_conditions",
            "Dry"
        )

        weather = data.get(
            "weather_conditions",
            "Normal"
        )

        light = data.get(
            "light_conditions",
            "Daylight"
        )

        age_band = data.get(
            "age_band_of_driver",
            "31-50"
        )

        driving_experience = data.get(
            "driving_experience",
            "2-5yr"
        )


        # =================================================
        # BASIC VALIDATION
        # =================================================

        if vehicles < 1 or vehicles > 20:

            return jsonify({
                "success": False,
                "message":
                    "Number of vehicles must be between 1 and 20"
            }), 400


        # =================================================
        # MODEL EXPECTED FEATURES
        # =================================================

        expected_features = list(
            preprocessor.feature_names_in_
        )


        # Create empty row
        row = {
            feature: None
            for feature in expected_features
        }


        # =================================================
        # USER-PROVIDED VALUES
        # =================================================

        user_values = {

            "Number_of_vehicles_involved":
                vehicles,

            "Type_of_vehicle":
                vehicle_type,

            "Type_of_collision":
                collision,

            "Road_surface_conditions":
                road_surface,

            "Weather_conditions":
                weather,

            "Light_conditions":
                light,

            "Age_band_of_driver":
                age_band,

            "Driving_experience":
                driving_experience,

            # UI lo hour field remove chesam,
            # so fixed default value.
            "Hour":
                12
        }


        for feature, value in user_values.items():

            if feature in row:

                row[feature] = value


        # =================================================
        # DEFAULT VALUES FOR FEATURES NOT SHOWN IN UI
        # =================================================

        categorical_defaults = {

            "Day_of_week":
                "Monday",

            "Sex_of_driver":
                "Male",

            "Educational_level":
                "Junior high school",

            "Vehicle_driver_relation":
                "Employee",

            "Owner_of_vehicle":
                "Owner",

            "Service_year_of_vehicle":
                "2-5yrs",

            "Defect_of_vehicle":
                "No defect",

            "Area_accident_occured":
                "Other",

            "Lanes_or_Medians":
                "Two-way (divided with solid lines road marking)",

            "Road_allignment":
                "Tangent road with flat terrain",

            "Types_of_Junction":
                "No junction",

            "Road_surface_type":
                "Asphalt roads",

            "Vehicle_movement":
                "Going straight",

            "Casualty_class":
                "Driver or rider",

            "Sex_of_casualty":
                "Male",

            "Age_band_of_casualty":
                "31-50",

            "Cause_of_accident":
                "No distancing"
        }


        for feature, value in categorical_defaults.items():

            if (
                feature in row
                and row[feature] is None
            ):

                row[feature] = value


        # =================================================
        # CREATE DATAFRAME
        # =================================================

        input_df = pd.DataFrame(
            [row],
            columns=expected_features
        )


        # =================================================
        # PREPROCESS INPUT
        # =================================================

        transformed = preprocessor.transform(
            input_df
        )


        # =================================================
        # ML PREDICTION
        # =================================================

        prediction_encoded = model.predict(
            transformed
        )[0]


        predicted_severity = (
            accident_label_encoder
            .inverse_transform(
                [prediction_encoded]
            )[0]
        )


        # =================================================
        # RISK LEVEL
        # =================================================

        severity_text = str(
            predicted_severity
        ).lower()


        if "fatal" in severity_text:

            risk_level = "Critical"

        elif "serious" in severity_text:

            risk_level = "High"

        else:

            risk_level = "Medium"


        # =================================================
        # SAVE PREDICTION
        # =================================================

        connection = database.get_connection()

        if connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO predictions
                (
                    module,
                    prediction_value,
                    risk_level,
                    model_name
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    "accidents",
                    str(predicted_severity),
                    risk_level,
                    "Accident Severity ML Model"
                )
            )

            connection.commit()

            cursor.close()
            connection.close()


        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "success": True,

            "module":
                "Accident Severity",

            "prediction": {

                "severity":
                    str(predicted_severity),

                "risk_level":
                    risk_level
            },

            "input": {

                "number_of_vehicles_involved":
                    vehicles,

                "type_of_vehicle":
                    vehicle_type,

                "type_of_collision":
                    collision,

                "road_surface_conditions":
                    road_surface,

                "weather_conditions":
                    weather,

                "light_conditions":
                    light,

                "age_band_of_driver":
                    age_band,

                "driving_experience":
                    driving_experience
            },

            "prediction_type":
                "ML",

            "model":
                "Accident Severity ML Model",

            "message":
                "Accident severity predicted successfully"
        })


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        return jsonify({

            "success": False,

            "message":
                "Accident ML prediction failed",

            "error":
                str(e)

        }), 500