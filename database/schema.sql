-- ============================================================
-- SMART CITY DIGITAL TWIN - DATABASE SETUP
-- ============================================================
-- The project .env uses DB_NAME=smart, so this schema uses the
-- same database name. This avoids the previous smart vs
-- smart_city_digital_twin mismatch.
--
-- Run this file once in MySQL/phpMyAdmin.
-- ============================================================

CREATE DATABASE IF NOT EXISTS smart
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE smart;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin','operator','viewer') DEFAULT 'operator',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS city_zones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    zone_code VARCHAR(50) NOT NULL UNIQUE,
    zone_name VARCHAR(120) NOT NULL,
    zone_type VARCHAR(50) NOT NULL,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    status VARCHAR(30) DEFAULT 'normal',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_zone_status(status)
);

CREATE TABLE IF NOT EXISTS infrastructure (
    id INT AUTO_INCREMENT PRIMARY KEY,
    zone_id INT NULL,
    name VARCHAR(150) NOT NULL,
    type VARCHAR(60) NOT NULL,
    status VARCHAR(40) DEFAULT 'operational',
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_infra_zone FOREIGN KEY(zone_id) REFERENCES city_zones(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS predictions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    module VARCHAR(50) NOT NULL,
    prediction_value VARCHAR(255) NOT NULL,
    risk_level VARCHAR(30),
    model_name VARCHAR(100),
    confidence DECIMAL(6,3),
    prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_prediction_module_time(module, prediction_time)
);

CREATE TABLE IF NOT EXISTS alerts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    module VARCHAR(50) NOT NULL,
    title VARCHAR(180) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(30) NOT NULL,
    value DECIMAL(15,4) NULL,
    threshold DECIMAL(15,4) NULL,
    status VARCHAR(30) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    INDEX idx_alert_status(status)
);

CREATE TABLE IF NOT EXISTS simulation_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    traffic_change DECIMAL(8,2) DEFAULT 0,
    air_quality_change DECIMAL(8,2) DEFAULT 0,
    energy_change DECIMAL(8,2) DEFAULT 0,
    overall_impact DECIMAL(8,2),
    city_status VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(120) NOT NULL,
    module VARCHAR(60),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS reports (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(60) NOT NULL,
    report_title VARCHAR(180) NOT NULL,
    file_path VARCHAR(500),
    generated_by INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_report_user FOREIGN KEY(generated_by) REFERENCES users(id) ON DELETE SET NULL
);

-- ============================================================
-- DEMO DIGITAL-TWIN ZONES
-- ============================================================
-- These are visualization zones for the Digital Twin map.
-- They do NOT alter or retrain any ML model.
-- Coordinates follow the map center already used by the project.
-- ============================================================

INSERT IGNORE INTO city_zones
(zone_code, zone_name, zone_type, latitude, longitude, status)
VALUES
('Z-CENTRAL', 'Central Zone', 'central', 16.5062000, 80.6480000, 'normal'),
('Z-RESIDENTIAL', 'Residential Zone', 'residential', 16.5153000, 80.6365000, 'normal'),
('Z-COMMERCIAL', 'Commercial Zone', 'commercial', 16.4998000, 80.6608000, 'warning'),
('Z-DANGER', 'Industrial Danger Zone', 'industrial', 16.4922000, 80.6755000, 'critical');

-- Demo infrastructure points used by the Digital Twin view.
INSERT INTO infrastructure (zone_id, name, type, status, latitude, longitude)
SELECT id, 'Central Traffic Junction', 'traffic_junction', 'operational', 16.5062000, 80.6480000
FROM city_zones z WHERE z.zone_code='Z-CENTRAL'
AND NOT EXISTS (SELECT 1 FROM infrastructure i WHERE i.name='Central Traffic Junction');

INSERT INTO infrastructure (zone_id, name, type, status, latitude, longitude)
SELECT id, 'City Power Substation', 'power', 'operational', 16.5153000, 80.6365000
FROM city_zones z WHERE z.zone_code='Z-RESIDENTIAL'
AND NOT EXISTS (SELECT 1 FROM infrastructure i WHERE i.name='City Power Substation');

INSERT INTO infrastructure (zone_id, name, type, status, latitude, longitude)
SELECT id, 'Commercial Monitoring Hub', 'monitoring', 'operational', 16.4998000, 80.6608000
FROM city_zones z WHERE z.zone_code='Z-COMMERCIAL'
AND NOT EXISTS (SELECT 1 FROM infrastructure i WHERE i.name='Commercial Monitoring Hub');

INSERT INTO infrastructure (zone_id, name, type, status, latitude, longitude)
SELECT id, 'Industrial Safety Sensor', 'safety_sensor', 'warning', 16.4922000, 80.6755000
FROM city_zones z WHERE z.zone_code='Z-DANGER'
AND NOT EXISTS (SELECT 1 FROM infrastructure i WHERE i.name='Industrial Safety Sensor');

-- ============================================================
-- ADMIN USER
-- ============================================================
-- The Flask application automatically creates the default admin
-- using ADMIN_EMAIL / ADMIN_PASSWORD from .env. No plain-text
-- password is stored by this SQL file.
-- ============================================================
