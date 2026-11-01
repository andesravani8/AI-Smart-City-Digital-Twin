from .dashboard import dashboard_bp
from .traffic import traffic_bp
from .air_quality import air_quality_bp
from .accidents import accidents_bp
from .energy import energy_bp
from .weather import weather_bp
from .digital_twin import digital_twin_bp
from .simulator import simulator_bp
from .assistant import assistant_bp
from .alerts import alerts_bp
from .reports import reports_bp


def register_routes(app):

    app.register_blueprint(
        dashboard_bp,
        url_prefix="/api/dashboard"
    )

    app.register_blueprint(
        traffic_bp,
        url_prefix="/api/traffic"
    )

    app.register_blueprint(
        air_quality_bp,
        url_prefix="/api/air-quality"
    )

    app.register_blueprint(
        accidents_bp,
        url_prefix="/api/accidents"
    )

    app.register_blueprint(
        energy_bp,
        url_prefix="/api/energy"
    )

    app.register_blueprint(
        weather_bp,
        url_prefix="/api/weather"
    )

    app.register_blueprint(
        digital_twin_bp,
        url_prefix="/api/digital-twin"
    )

    app.register_blueprint(
        simulator_bp,
        url_prefix="/api/simulator"
    )

    app.register_blueprint(
        assistant_bp,
        url_prefix="/api/assistant"
    )

    app.register_blueprint(
        alerts_bp,
        url_prefix="/api/alerts"
    )

    app.register_blueprint(
        reports_bp,
        url_prefix="/api/reports"
    )