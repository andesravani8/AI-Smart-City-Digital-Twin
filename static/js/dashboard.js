// ============================================================
// SMART CITY DIGITAL TWIN
// DASHBOARD JAVASCRIPT
// ============================================================


// ============================================================
// GLOBAL DASHBOARD DATA
// ============================================================

let dashboardData = null;


// ============================================================
// LOAD DASHBOARD DATA FROM API
// ============================================================

async function loadDashboardData() {

    try {

        const response = await fetch(
            "/api/dashboard/summary"
        );

        if (!response.ok) {

            throw new Error(
                `HTTP Error: ${response.status}`
            );

        }

        const data = await response.json();

        console.log(
            "Dashboard API Response:",
            data
        );


        if (!data.success) {

            console.error(
                "Dashboard API Error:",
                data.message
            );

            return;

        }


        dashboardData = data;


        // Update all dashboard sections

        updateSummary(data);

        updateAlerts(data);

        updateZoneInformation(data);

        updateAIInsight(data);


    }

    catch (error) {

        console.error(
            "Unable to load dashboard data:",
            error
        );

    }

}


// ============================================================
// UPDATE SUMMARY CARDS
// ============================================================

function updateSummary(data) {

    const summary = data.summary;


    // ----------------------------------------
    // Total Zones
    // ----------------------------------------

    const totalZones =
        document.getElementById(
            "total-zones"
        );

    if (totalZones) {

        totalZones.textContent =
            summary.total_zones ?? 0;

    }


    // ----------------------------------------
    // Active Alerts
    // ----------------------------------------

    const activeAlerts =
        document.getElementById(
            "active-alerts"
        );

    if (activeAlerts) {

        activeAlerts.textContent =
            summary.active_alerts ?? 0;

    }


    // ----------------------------------------
    // Sidebar Alert Count
    // ----------------------------------------

    const sidebarAlertCount =
        document.getElementById(
            "sidebar-alert-count"
        );

    if (sidebarAlertCount) {

        sidebarAlertCount.textContent =
            summary.active_alerts ?? 0;

    }


    // ----------------------------------------
    // Infrastructure
    // ----------------------------------------

    const infrastructure =
        document.getElementById(
            "total-infrastructure"
        );

    if (infrastructure) {

        infrastructure.textContent =
            summary.total_infrastructure ?? 0;

    }


    // ----------------------------------------
    // Total Predictions
    // ----------------------------------------

    const predictions =
        document.getElementById(
            "total-predictions"
        );

    if (predictions) {

        predictions.textContent =
            summary.total_predictions ?? 0;

    }

}


// ============================================================
// UPDATE ALERTS
// ============================================================

function updateAlerts(data) {

    const alertsContainer =
        document.getElementById(
            "dashboard-alerts"
        );


    if (!alertsContainer) {
        return;
    }


    const alerts =
        data.recent_alerts || [];


    // No alerts

    if (alerts.length === 0) {

        alertsContainer.innerHTML = `

            <div class="alert-item info">

                <div class="alert-icon">

                    <i class="bi bi-check-circle-fill"></i>

                </div>

                <div class="alert-content">

                    <strong>
                        No active alerts
                    </strong>

                    <span>
                        City conditions are currently stable.
                    </span>

                    <small>
                        Just now
                    </small>

                </div>

                <span class="severity info">
                    OK
                </span>

            </div>

        `;

        return;

    }


    // Clear old alerts

    alertsContainer.innerHTML = "";


    // Add database alerts

    alerts.forEach(alert => {

        const severity =
            alert.severity || "low";


        const icon =
            getAlertIcon(
                alert.module
            );


        const time =
            formatAlertTime(
                alert.created_at
            );


        const alertHTML = `

            <div class="alert-item ${severity}">

                <div class="alert-icon">

                    <i class="bi ${icon}"></i>

                </div>


                <div class="alert-content">

                    <strong>
                        ${escapeHTML(
                            alert.title
                        )}
                    </strong>


                    <span>
                        ${escapeHTML(
                            alert.message || ""
                        )}
                    </span>


                    <small>
                        ${time}
                    </small>

                </div>


                <span class="severity ${severity}">

                    ${severity.toUpperCase()}

                </span>

            </div>

        `;


        alertsContainer.insertAdjacentHTML(
            "beforeend",
            alertHTML
        );

    });

}


// ============================================================
// ALERT ICON
// ============================================================

function getAlertIcon(module) {

    switch (
        String(module || "").toLowerCase()
    ) {

        case "traffic":
            return "bi-car-front-fill";

        case "air":
        case "air_quality":
        case "air-quality":
            return "bi-cloud-haze2-fill";

        case "accident":
        case "accidents":
            return "bi-exclamation-triangle-fill";

        case "energy":
            return "bi-lightning-charge-fill";

        case "weather":
            return "bi-cloud-sun-fill";

        default:
            return "bi-info-circle-fill";

    }

}


// ============================================================
// ZONE INFORMATION
// ============================================================

function updateZoneInformation(data) {

    const zoneStatus =
        data.zone_status || [];


    console.log(
        "Zone Status:",
        zoneStatus
    );

}


// ============================================================
// AI CITY INSIGHT
// ============================================================

function updateAIInsight(data) {

    const insight =
        document.getElementById(
            "ai-city-insight"
        );


    if (!insight) {
        return;
    }


    const summary =
        data.summary;


    if (
        summary.active_alerts &&
        summary.active_alerts > 0
    ) {

        insight.textContent =
            `${summary.active_alerts} active alert(s) detected. ` +
            `The AI monitoring system is analyzing current city conditions.`;

    }

    else {

        insight.textContent =
            "AI is continuously analyzing traffic, " +
            "air quality, energy and weather patterns. " +
            "No major city-wide issues are currently detected.";

    }

}


// ============================================================
// FORMAT ALERT TIME
// ============================================================

function formatAlertTime(dateValue) {

    if (!dateValue) {
        return "Recently";
    }


    const date =
        new Date(dateValue);


    if (isNaN(date.getTime())) {
        return "Recently";
    }


    const now =
        new Date();


    const difference =
        Math.floor(
            (now - date) / 60000
        );


    if (difference < 1) {

        return "Just now";

    }


    if (difference < 60) {

        return `${difference} min ago`;

    }


    const hours =
        Math.floor(
            difference / 60
        );


    if (hours < 24) {

        return `${hours} hour${hours > 1 ? "s" : ""} ago`;

    }


    const days =
        Math.floor(
            hours / 24
        );


    return `${days} day${days > 1 ? "s" : ""} ago`;

}


// ============================================================
// SECURITY HELPER
// ============================================================

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value ?? "";

    return div.innerHTML;

}


// ============================================================
// LIVE DATE & TIME
// ============================================================

function updateDateTime() {

    const dateElement =
        document.getElementById(
            "currentDate"
        );


    const timeElement =
        document.getElementById(
            "currentTime"
        );


    const now =
        new Date();


    if (dateElement) {

        dateElement.textContent =
            now.toLocaleDateString(
                "en-IN",
                {
                    weekday: "long",
                    month: "long",
                    day: "numeric"
                }
            );

    }


    if (timeElement) {

        timeElement.textContent =
            now.toLocaleTimeString(
                "en-IN",
                {
                    hour12: false
                }
            );

    }

}


// ============================================================
// AUTO REFRESH
// ============================================================

function startDashboardRefresh() {

    // Refresh every 30 seconds

    setInterval(
        loadDashboardData,
        30000
    );

}


// ============================================================
// PAGE INITIALIZATION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "Smart City Dashboard initialized."
        );


        // Load database data

        loadDashboardData();


        // Start clock

        updateDateTime();


        // Update clock every second

        setInterval(
            updateDateTime,
            1000
        );


        // Start API refresh

        startDashboardRefresh();

    }
);