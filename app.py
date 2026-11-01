# ============================================================
# MACHINE LEARNING-BASED SMART CITY DIGITAL TWIN
# MAIN FLASK APPLICATION
# ============================================================

import os
from functools import wraps

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from flask_cors import CORS
from dotenv import load_dotenv

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from utils.model_loader import model_loader
from backend.routes import register_routes


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# CREATE FLASK APP
# ============================================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "smart-city-digital-twin-secret-key"
)

CORS(app)

app.config["JSON_SORT_KEYS"] = False


# ============================================================
# LOGIN REQUIRED DECORATOR
# ============================================================

def login_required(view_function):
    """
    Protect frontend pages.
    User must login before accessing the application pages.
    """

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login to access the Smart City Dashboard.",
                "warning"
            )

            return redirect(
                url_for("login_page")
            )

        return view_function(
            *args,
            **kwargs
        )

    return wrapped_view


# ============================================================
# LOAD MACHINE LEARNING MODELS
# ============================================================

print("=" * 60)
print("LOADING MACHINE LEARNING MODELS")
print("=" * 60)

try:

    model_loader.load_all()

    print("ML Model Status:")
    print(model_loader.status())

except Exception as e:

    print(
        "WARNING: ML model loading error:",
        e
    )


print("=" * 60)


# ============================================================
# REGISTER BACKEND API ROUTES
# ============================================================

register_routes(app)


# ============================================================
# DATABASE HELPER
# ============================================================

def get_database_connection():

    """
    Returns MySQL connection using the existing
    backend.database Database class.
    """

    from backend.database import database

    return database.get_connection()


# ============================================================
# HOME / ROOT
# ============================================================

@app.route("/")
def home():

    # --------------------------------------------------------
    # Already logged in
    # --------------------------------------------------------

    if "user_id" in session:

        return redirect(
            url_for("dashboard_page")
        )


    # --------------------------------------------------------
    # Not logged in
    # --------------------------------------------------------

    return redirect(
        url_for("login_page")
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login_page():

    # --------------------------------------------------------
    # If already logged in
    # --------------------------------------------------------

    if "user_id" in session:

        return redirect(
            url_for("dashboard_page")
        )


    # --------------------------------------------------------
    # POST LOGIN
    # --------------------------------------------------------

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not email or not password:

            flash(
                "Please enter email and password.",
                "danger"
            )

            return redirect(
                url_for("login_page")
            )


        connection = None
        cursor = None


        try:

            # ------------------------------------------------
            # DATABASE CONNECTION
            # ------------------------------------------------

            connection = get_database_connection()


            if connection is None:

                flash(
                    "Unable to connect to MySQL database.",
                    "danger"
                )

                return redirect(
                    url_for("login_page")
                )


            # ------------------------------------------------
            # GET USER
            # ------------------------------------------------

            cursor = connection.cursor(
                dictionary=True
            )


            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    email,
                    password_hash,
                    role
                FROM users
                WHERE email = %s
                LIMIT 1
                """,
                (email,)
            )


            user = cursor.fetchone()


            # ------------------------------------------------
            # USER NOT FOUND
            # ------------------------------------------------

            if user is None:

                flash(
                    "Invalid email or password.",
                    "danger"
                )

                return redirect(
                    url_for("login_page")
                )


            # ------------------------------------------------
            # CHECK PASSWORD
            # ------------------------------------------------

            password_hash = user.get(
                "password_hash"
            )


            if not password_hash:

                flash(
                    "This user account has no valid password.",
                    "danger"
                )

                return redirect(
                    url_for("login_page")
                )


            if not check_password_hash(
                password_hash,
                password
            ):

                flash(
                    "Invalid email or password.",
                    "danger"
                )

                return redirect(
                    url_for("login_page")
                )


            # ------------------------------------------------
            # LOGIN SUCCESS
            # ------------------------------------------------

            session.clear()


            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            session["user_email"] = user["email"]

            session["user_role"] = user["role"]


            flash(
                "Login successful. Welcome to Smart City Digital Twin.",
                "success"
            )


            return redirect(
                url_for("dashboard_page")
            )


        except Exception as e:

            print(
                "LOGIN ERROR:",
                e
            )


            flash(
                "Login failed. Please check the database connection.",
                "danger"
            )


            return redirect(
                url_for("login_page")
            )


        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass


            if connection:

                try:
                    connection.close()
                except Exception:
                    pass


    # --------------------------------------------------------
    # GET LOGIN PAGE
    # --------------------------------------------------------

    return render_template(
        "login.html"
    )


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register_page():

    # --------------------------------------------------------
    # Already logged in
    # --------------------------------------------------------

    if "user_id" in session:

        return redirect(
            url_for("dashboard_page")
        )


    # --------------------------------------------------------
    # POST REGISTER
    # --------------------------------------------------------

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not name or not email or not password:

            flash(
                "All fields are required.",
                "danger"
            )

            return redirect(
                url_for("register_page")
            )


        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("register_page")
            )


        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "danger"
            )

            return redirect(
                url_for("register_page")
            )


        connection = None
        cursor = None


        try:

            # ------------------------------------------------
            # CONNECT DATABASE
            # ------------------------------------------------

            connection = get_database_connection()


            if connection is None:

                flash(
                    "Unable to connect to MySQL database.",
                    "danger"
                )

                return redirect(
                    url_for("register_page")
                )


            cursor = connection.cursor(
                dictionary=True
            )


            # ------------------------------------------------
            # CHECK EXISTING USER
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = %s
                LIMIT 1
                """,
                (email,)
            )


            existing_user = cursor.fetchone()


            if existing_user:

                flash(
                    "An account with this email already exists.",
                    "warning"
                )

                return redirect(
                    url_for("register_page")
                )


            # ------------------------------------------------
            # HASH PASSWORD
            # ------------------------------------------------

            hashed_password = generate_password_hash(
                password
            )


            # ------------------------------------------------
            # INSERT USER
            # ------------------------------------------------

            cursor.execute(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password_hash,
                    role
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    name,
                    email,
                    hashed_password,
                    "operator"
                )
            )


            connection.commit()


            flash(
                "Account created successfully. Please login.",
                "success"
            )


            return redirect(
                url_for("login_page")
            )


        except Exception as e:

            print(
                "REGISTER ERROR:",
                e
            )


            if connection:

                try:
                    connection.rollback()
                except Exception:
                    pass


            flash(
                "Registration failed. Please check the database.",
                "danger"
            )


            return redirect(
                url_for("register_page")
            )


        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass


            if connection:

                try:
                    connection.close()
                except Exception:
                    pass


    # --------------------------------------------------------
    # GET REGISTER PAGE
    # --------------------------------------------------------

    return render_template(
        "register.html"
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard_page():

    return render_template(
        "dashboard.html",
        user_name=session.get(
            "user_name",
            "User"
        ),
        user_email=session.get(
            "user_email",
            ""
        ),
        user_role=session.get(
            "user_role",
            "operator"
        )
    )


# ============================================================
# TRAFFIC PAGE
# ============================================================

@app.route("/traffic")
@login_required
def traffic_page():

    return render_template(
        "modules/traffic.html"
    )


# ============================================================
# AIR QUALITY PAGE
# ============================================================

@app.route("/air-quality")
@login_required
def air_quality_page():

    return render_template(
        "modules/air_quality.html"
    )


# ============================================================
# ACCIDENTS PAGE
# ============================================================

@app.route("/accidents")
@login_required
def accidents_page():

    return render_template(
        "modules/accidents.html"
    )


# ============================================================
# ENERGY PAGE
# ============================================================

@app.route("/energy")
@login_required
def energy_page():

    return render_template(
        "modules/energy.html"
    )


# ============================================================
# WEATHER PAGE
# ============================================================

@app.route("/weather")
@login_required
def weather_page():

    return render_template(
        "modules/weather.html"
    )


# ============================================================
# DIGITAL TWIN PAGE
# ============================================================

@app.route("/digital-twin")
@login_required
def digital_twin_page():

    return render_template(
        "digital_twin.html"
    )


# ============================================================
# SIMULATOR PAGE
# ============================================================

@app.route("/simulator")
@login_required
def simulator_page():

    return render_template(
        "simulator.html"
    )


# ============================================================
# AI ASSISTANT PAGE
# ============================================================

@app.route("/assistant")
@login_required
def assistant_page():

    return render_template(
        "ai_assistant.html"
    )


# ============================================================
# ALERTS PAGE
# ============================================================

@app.route("/alerts")
@login_required
def alerts_page():

    return render_template(
        "alerts.html"
    )


# ============================================================
# REPORTS PAGE
# ============================================================

@app.route("/reports")
@login_required
def reports_page():

    return render_template(
        "reports.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()


    flash(
        "You have been logged out successfully.",
        "success"
    )


    return redirect(
        url_for("login_page")
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({

        "success": True,

        "status": "online",

        "project":
            "Machine Learning-Based Smart City Digital Twin"

    })


# ============================================================
# ML MODEL STATUS
# ============================================================

@app.route("/api/model-status")
def model_status():

    try:

        return jsonify({

            "success": True,

            "models":
                model_loader.status()

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message":
                str(e)

        }), 500


# ============================================================
# DATABASE CONNECTION TEST
# ============================================================

@app.route("/api/database-test")
def database_test():

    connection = None


    try:

        connection = get_database_connection()


        if connection:

            connection.close()


            return jsonify({

                "success": True,

                "message":
                    "MySQL database connected successfully"

            })


        return jsonify({

            "success": False,

            "message":
                "Database connection failed"

        }), 500


    except Exception as e:

        print(
            "Database test error:",
            e
        )


        return jsonify({

            "success": False,

            "message":
                str(e)

        }), 500


    finally:

        if connection:

            try:
                connection.close()
            except Exception:
                pass


# ============================================================
# 404 ERROR HANDLER
# ============================================================

@app.errorhandler(404)
def not_found(error):

    # --------------------------------------------------------
    # API 404
    # --------------------------------------------------------

    if request.path.startswith(
        "/api/"
    ):

        return jsonify({

            "success": False,

            "message":
                "API endpoint not found"

        }), 404


    # --------------------------------------------------------
    # FRONTEND 404
    # --------------------------------------------------------

    return render_template(
        "404.html"
    ), 404


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    print()

    print("=" * 60)

    print(
        " MACHINE LEARNING-BASED SMART CITY DIGITAL TWIN"
    )

    print("=" * 60)

    print(
        " Server     : http://127.0.0.1:5000"
    )

    print(
        " Login      : http://127.0.0.1:5000/login"
    )

    print(
        " Dashboard  : http://127.0.0.1:5000/"
    )

    print(
        " Health API : http://127.0.0.1:5000/api/health"
    )

    print(
        " Model API  : http://127.0.0.1:5000/api/model-status"
    )

    print(
        " Database   : http://127.0.0.1:5000/api/database-test"
    )

    print()

    print(
        " ML APIs"
    )

    print("-" * 60)

    print(
        " Traffic    : /api/traffic/predict"
    )

    print(
        " Air Quality: /api/air-quality/predict"
    )

    print(
        " Accidents  : /api/accidents/predict"
    )

    print(
        " Energy     : /api/energy/predict"
    )

    print(
        " Weather    : /api/weather/predict"
    )

    print("=" * 60)


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )