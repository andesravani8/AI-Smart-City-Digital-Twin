document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("accidentForm");
    if (!form) return;

    const loading = document.getElementById("accidentLoading");
    const errorBox = document.getElementById("accidentError");
    const resultCard = document.getElementById("accidentResult");
    const severityResult = document.getElementById("severityResult");
    const modelResult = document.getElementById("accidentModel");
    const riskResult = document.getElementById("accidentRisk");
    const button = document.getElementById("predictAccidentBtn");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        errorBox.style.display = "none";
        resultCard.style.display = "none";
        loading.style.display = "block";
        button.disabled = true;

        const hour = Number(document.getElementById("hour").value);
        const vehicles = Number(document.getElementById("number_of_vehicles_involved").value);
        const vehicleType = document.getElementById("type_of_vehicle").value;
        const collision = document.getElementById("type_of_collision").value;
        const roadSurface = document.getElementById("road_surface_conditions").value;
        const weather = document.getElementById("weather_conditions").value;
        const light = document.getElementById("light_conditions").value;
        const ageBand = document.getElementById("age_band_of_driver").value;
        const experience = document.getElementById("driving_experience").value;

        if (!Number.isInteger(hour) || hour < 0 || hour > 23) {
            showError("Hour must be between 0 and 23.");
            return finish();
        }
        if (!Number.isInteger(vehicles) || vehicles < 1 || vehicles > 20) {
            showError("Number of vehicles must be between 1 and 20.");
            return finish();
        }

        try {
            const response = await fetch("/api/accidents/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    hour,
                    driving_experience: experience,
                    type_of_vehicle: vehicleType,
                    weather_conditions: weather,
                    type_of_collision: collision,
                    number_of_vehicles_involved: vehicles,
                    road_surface_conditions: roadSurface,
                    light_conditions: light,
                    age_band_of_driver: ageBand
                })
            });

            const data = await response.json();
            if (!response.ok || !data.success) {
                throw new Error(data.message || data.error || "Accident severity prediction failed.");
            }

            const prediction = data.prediction || {};
            const severity = prediction.severity || prediction.accident_severity || prediction.predicted_severity || "--";
            const risk = prediction.risk_level || data.risk_level || "--";

            severityResult.textContent = severity;
            riskResult.textContent = risk;
            modelResult.textContent = data.model || "Accident Severity ML Model";

            const text = String(severity).toLowerCase();
            severityResult.classList.remove("low", "medium", "high", "critical");
            riskResult.classList.remove("low", "medium", "high", "critical");

            const riskClass = String(risk).toLowerCase();
            if (["low", "medium", "high", "critical"].includes(riskClass)) {
                riskResult.classList.add(riskClass);
            } else if (text.includes("fatal")) {
                severityResult.classList.add("critical");
            } else if (text.includes("serious")) {
                severityResult.classList.add("high");
            } else {
                severityResult.classList.add("medium");
            }

            resultCard.style.display = "block";
        } catch (error) {
            console.error("Accident prediction error:", error);
            showError(error.message || "Unable to predict accident severity.");
        } finally {
            finish();
        }
    });

    function showError(message) {
        errorBox.textContent = message;
        errorBox.style.display = "block";
    }

    function finish() {
        loading.style.display = "none";
        button.disabled = false;
    }
});
