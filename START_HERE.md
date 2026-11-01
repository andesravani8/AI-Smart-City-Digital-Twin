# Smart City Digital Twin — Final Update

## What was changed

- Added a real local admin login with MySQL-backed authentication.
- Added a `backend/auth/` folder for login/logout/session handling.
- Added animated futuristic login UI under `templates/login.html` and `static/css/auth/`.
- Added Digital Twin zone overlays: Central, Residential, Commercial/Warning, and Industrial/Danger.
- Fixed the Digital Twin frontend field names to use the database API fields (`zone_name`, `zone_type`).
- Added zone labels, colored circles, status legend, infrastructure markers, and zone-click navigation.
- Fixed City Reports so it reads the five existing dataset files directly from `data/`.
- Aligned the database setup with `.env` using `DB_NAME=smart`.
- Added automatic default-admin creation and automatic Digital Twin demo-zone creation when the database tables exist.

## What was deliberately NOT changed

The following existing ML files were left unchanged:

- Traffic model, preprocessor, route and frontend
- Air Quality model, preprocessor, route and frontend
- Accident model, preprocessor, route and frontend
- Energy model, preprocessor, route and frontend
- Weather model, preprocessor, route and frontend

No ML model is retrained by these changes.

## First-time setup

1. Start XAMPP/MySQL.
2. Open phpMyAdmin.
3. Run `database/schema.sql`.
4. Open this project folder in VS Code.
5. Create/activate your Python virtual environment.
6. Run:

```bash
pip install -r requirements.txt
python app.py
```

7. Open:

`http://127.0.0.1:5000/`

## Default local login

Email: `admin@smartcity.local`

Password: `Admin@123`

These values come from `.env`. Change them if needed.

## Important database note

The project `.env` is set to:

`DB_NAME=smart`

This intentionally matches the database name in `database/schema.sql` so the previous `smart` vs `smart_city_digital_twin` mismatch does not happen again.

## Digital Twin note

The colored zones are Digital Twin visualization/database zones. They are not ML training data and do not change the five ML prediction models.
