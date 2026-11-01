from flask import Blueprint, request, jsonify
import pandas as pd
import joblib
import os

from backend.services.alert_service import alert_service


traffic_bp = Blueprint(
    "traffic",
    __name__,
    url_prefix="/api/traffic"
)


# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "traffic_model.joblib"
)

PREPROCESSOR_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "traffic_preprocessor.joblib"
)


# ============================================================
# LOAD MODEL
# ============================================================

traffic_model = None
traffic_preprocessor = None

try:
    traffic_model = joblib.load(MODEL_PATH)
    traffic_preprocessor = joblib.load(PREPROCESSOR_PATH)

    print("Traffic ML model loaded successfully.")

except Exception as e:

    print("Traffic model loading error:", e)


# ============================================================
# TRAFFIC PREDICTION
# ============================================================

@traffic_bp.route("/predict", methods=["POST"])
def predict_traffic():

    try:

        # ----------------------------------------------------
        # CHECK MODEL
        # ----------------------------------------------------

        if traffic_model is None or traffic_preprocessor is None:

            return jsonify({
                "success": False,
                "error": "Traffic ML model is not loaded."
            }), 500


        # ----------------------------------------------------
        # GET JSON DATA
        # ----------------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "Request data is required."
            }), 400


        # ----------------------------------------------------
        # READ INPUTS
        # ----------------------------------------------------

        junction = data.get("junction")

        hour = data.get("hour")

        day = data.get("day")

        month = data.get("month")

        day_of_week = data.get("day_of_week")

        is_weekend = data.get("is_weekend")

        current_vehicles = data.get(
            "current_vehicles",
            data.get("currentVehicles")
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if junction is None:
            return jsonify({
                "success": False,
                "error": "Junction is required."
            }), 400

        if hour is None:
            return jsonify({
                "success": False,
                "error": "Hour is required."
            }), 400

        if day is None:
            return jsonify({
                "success": False,
                "error": "Day is required."
            }), 400

        if month is None:
            return jsonify({
                "success": False,
                "error": "Month is required."
            }), 400

        if day_of_week is None:
            return jsonify({
                "success": False,
                "error": "Day of week is required."
            }), 400

        if is_weekend is None:
            return jsonify({
                "success": False,
                "error": "Weekend value is required."
            }), 400


        # ----------------------------------------------------
        # CONVERT NUMERIC VALUES
        # ----------------------------------------------------

        try:

            junction = int(junction)
            hour = int(hour)
            day = int(day)
            month = int(month)
            day_of_week = int(day_of_week)
            is_weekend = int(is_weekend)

            if current_vehicles is not None:
                current_vehicles = float(current_vehicles)

        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "error": "Invalid numeric input."
            }), 400


        # ----------------------------------------------------
        # RANGE VALIDATION
        # ----------------------------------------------------

        if junction < 1 or junction > 4:

            return jsonify({
                "success": False,
                "error": "Junction must be between 1 and 4."
            }), 400


        if hour < 0 or hour > 23:

            return jsonify({
                "success": False,
                "error": "Hour must be between 0 and 23."
            }), 400


        if day < 1 or day > 31:

            return jsonify({
                "success": False,
                "error": "Day must be between 1 and 31."
            }), 400


        if month < 1 or month > 12:

            return jsonify({
                "success": False,
                "error": "Month must be between 1 and 12."
            }), 400


        if day_of_week < 0 or day_of_week > 6:

            return jsonify({
                "success": False,
                "error": "Day of week must be between 0 and 6."
            }), 400


        if is_weekend not in [0, 1]:

            return jsonify({
                "success": False,
                "error": "Weekend value must be 0 or 1."
            }), 400


        if current_vehicles is not None and current_vehicles < 0:

            return jsonify({
                "success": False,
                "error": "Current vehicles cannot be negative."
            }), 400


        # ----------------------------------------------------
        # CREATE INPUT DATAFRAME
        # ----------------------------------------------------

        input_data = pd.DataFrame([{

            "Junction": junction,

            "hour": hour,

            "day": day,

            "month": month,

            "day_of_week": day_of_week,

            "is_weekend": is_weekend

        }])


        # ----------------------------------------------------
        # APPLY PREPROCESSOR
        # ----------------------------------------------------

        processed_data = traffic_preprocessor.transform(
            input_data
        )


        # ----------------------------------------------------
        # ML PREDICTION
        # ----------------------------------------------------

        prediction = traffic_model.predict(
            processed_data
        )


        predicted_vehicles = max(
            0.0,
            float(prediction[0])
        )


        # ====================================================
        # TRAFFIC CLASSIFICATION
        # ====================================================

        if predicted_vehicles < 30:

            congestion = "Low"
            risk = "Low"

        elif predicted_vehicles < 70:

            congestion = "Moderate"
            risk = "Medium"

        elif predicted_vehicles < 100:

            congestion = "High"
            risk = "High"

        else:

            congestion = "Severe"
            risk = "Critical"


        # ====================================================
        # CURRENT VS PREDICTED TRAFFIC
        # ====================================================

        deviation = None
        abnormal_traffic = False


        if current_vehicles is not None:

            if predicted_vehicles > 0:

                deviation = (
                    (
                        current_vehicles -
                        predicted_vehicles
                    )
                    /
                    predicted_vehicles
                ) * 100

            else:

                deviation = 0


            # ------------------------------------------------
            # ABNORMAL TRAFFIC
            # ------------------------------------------------

            if deviation >= 30:

                abnormal_traffic = True


        # ====================================================
        # ALERT GENERATION
        # ====================================================

        alert_created = False
        alert_messages = []


        try:

            # ------------------------------------------------
            # CRITICAL PREDICTED TRAFFIC
            # ------------------------------------------------

            if predicted_vehicles >= 100:

                alert = alert_service.create_alert(

                    module="traffic",

                    level="critical",

                    title="Critical Traffic Congestion",

                    message=(
                        f"Critical traffic congestion "
                        f"predicted at Junction {junction}. "
                        f"Expected vehicles: "
                        f"{predicted_vehicles:.1f}. "
                        f"Immediate attention is recommended."
                    ),

                    value=predicted_vehicles,

                    threshold=100
                )


                if alert:

                    alert_created = True

                    alert_messages.append(
                        "Critical traffic alert created."
                    )


            # ------------------------------------------------
            # HIGH PREDICTED TRAFFIC
            # ------------------------------------------------

            elif predicted_vehicles >= 70:

                alert = alert_service.create_alert(

                    module="traffic",

                    level="high",

                    title="High Traffic Congestion",

                    message=(
                        f"High traffic congestion "
                        f"predicted at Junction {junction}. "
                        f"Expected vehicles: "
                        f"{predicted_vehicles:.1f}."
                    ),

                    value=predicted_vehicles,

                    threshold=70
                )


                if alert:

                    alert_created = True

                    alert_messages.append(
                        "High traffic alert created."
                    )


            # ------------------------------------------------
            # ABNORMAL CURRENT TRAFFIC
            # ------------------------------------------------

            if abnormal_traffic:

                alert = alert_service.create_alert(

                    module="traffic",

                    level="critical",

                    title="Abnormal Traffic Detected",

                    message=(
                        f"Current traffic at Junction "
                        f"{junction} is "
                        f"{current_vehicles:.0f} vehicles, "
                        f"which is {deviation:.1f}% above "
                        f"the ML predicted value of "
                        f"{predicted_vehicles:.1f} vehicles."
                    ),

                    value=current_vehicles,

                    threshold=predicted_vehicles * 1.30
                )


                if alert:

                    alert_created = True

                    alert_messages.append(
                        "Abnormal traffic alert created."
                    )


        except Exception as alert_error:

            print(
                "Traffic alert generation error:",
                alert_error
            )


        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        response_data = {

            "success": True,

            "module": "traffic",

            "junction": junction,

            "hour": hour,

            "day": day,

            "month": month,

            "day_of_week": day_of_week,

            "is_weekend": is_weekend,

            "predicted_vehicles":
                round(predicted_vehicles, 2),

            "congestion":
                congestion,

            "risk":
                risk,

            "current_vehicles":
                (
                    round(current_vehicles, 2)
                    if current_vehicles is not None
                    else None
                ),

            "deviation_percentage":
                (
                    round(deviation, 2)
                    if deviation is not None
                    else None
                ),

            "abnormal_traffic":
                abnormal_traffic,

            "prediction_type":
                "ML",

            "alert_created":
                alert_created,

            "alert_messages":
                alert_messages
        }


        return jsonify(response_data), 200


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print(
            "Traffic prediction error:",
            e
        )

        return jsonify({

            "success": False,

            "error":
                "Traffic prediction failed.",

            "details":
                str(e)

        }), 500