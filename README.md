# AI-Powered Smart City Digital Twin

A Flask-based Smart City dashboard with five ML modules, Digital Twin map, alerts, what-if simulator, AI assistant and reporting APIs.

## Run locally

1. Open this folder in VS Code.
2. Create/activate a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the server:

```bash
python app.py
```

5. Open `http://127.0.0.1:5000/`.

## Important ML note

The supplied ZIP already contains the existing ML datasets and `.joblib` model files. The login and Digital Twin updates do not modify the five prediction models or their preprocessing logic.

Expected model names:

- `traffic_model.joblib` + `traffic_preprocessor.joblib`
- `air_quality_model.joblib` + `air_quality_preprocessor.joblib`
- `accident_model.joblib` + `accident_preprocessor.joblib`
- `energy_model.joblib` + `energy_preprocessor.joblib`
- `weather_model.joblib` + `weather_preprocessor.joblib`

Put them under `ml/models/`.

Existing dataset files:

- `data/traffic.csv`
- `data/air_quality.csv.csv`
- `data/Road.csv.csv`
- `data/Energy.csv.csv`
- `data/weather.csv.csv`

The Reports service now maps these exact existing files to the five modules.

## Main URLs

- Dashboard: `/`
- Traffic: `/traffic`
- Air Quality: `/air-quality`
- Accidents: `/accidents`
- Energy: `/energy`
- Weather: `/weather`
- Digital Twin: `/digital-twin`
- Simulator: `/simulator`
- AI Assistant: `/assistant`
- Alerts: `/alerts`
- Reports: `/reports`
- Health API: `/api/health`
- Dashboard API: `/api/dashboard/summary`

## Database

Run `database/schema.sql` in MySQL/phpMyAdmin to create the application tables. Set `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` and `DB_NAME` in `.env` when database integration is enabled.

## Local Login

The project now opens through a secure local administrator login before the dashboard.
The login uses the existing `users` table and stores a Werkzeug password hash, not a plain-text password.

Default local demo credentials are read from `.env`:

- Email: `admin@smartcity.local`
- Password: `Admin@123`

Change `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `.env` before sharing the project.

## Database setup

1. Start MySQL/XAMPP.
2. Open phpMyAdmin or MySQL.
3. Run `database/schema.sql` once.
4. Keep `.env` as `DB_NAME=smart` unless you intentionally use another database name.
5. Start Flask. The application automatically creates the default admin and ensures the four Digital Twin demo zones exist.

## Digital Twin zones

The Digital Twin map now draws logical zone overlays: Central, Residential, Commercial/Warning, and Industrial/Danger. These are visualization/database zones only; the five existing ML prediction models and their prediction routes are not modified.

## City Reports

The Reports page reads the project's actual files from `data/` using the existing dataset filenames, so the five datasets are shown as connected instead of incorrectly reporting `Dataset not connected yet`.
