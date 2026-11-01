// energy.js
// ============================================================
// ENERGY CONSUMPTION PREDICTION
// Machine Learning Based Smart City Digital Twin
// ============================================================


// ------------------------------------------------------------
// GET HTML ELEMENTS
// ------------------------------------------------------------

const energyForm = document.getElementById("energyForm");

const loading = document.getElementById("loading");

const errorBox = document.getElementById("errorBox");

const resultCard = document.getElementById("resultCard");

const predictButton = document.getElementById("predictButton");


// ------------------------------------------------------------
// FORM SUBMIT
// ------------------------------------------------------------

energyForm.addEventListener("submit", async function (event) {

    event.preventDefault();


    // --------------------------------------------------------
    // CLEAR PREVIOUS ERROR
    // --------------------------------------------------------

    errorBox.style.display = "none";
    errorBox.textContent = "";


    // --------------------------------------------------------
    // GET INPUT VALUES
    // --------------------------------------------------------

    const month =
        document.getElementById("month").value;

    const hour =
        document.getElementById("hour").value;

    const dayOfWeek =
        document.getElementById("day_of_week").value;

    const holiday =
        document.getElementById("holiday").value;

    const temperature =
        document.getElementById("temperature").value;

    const humidity =
        document.getElementById("humidity").value;

    const squareFootage =
        document.getElementById("square_footage").value;

    const occupancy =
        document.getElementById("occupancy").value;

    const hvacUsage =
        document.getElementById("hvac_usage").value;

    const lightingUsage =
        document.getElementById("lighting_usage").value;

    const renewableEnergy =
        document.getElementById("renewable_energy").value;


    // --------------------------------------------------------
    // VALIDATION
    // --------------------------------------------------------

    if (
        month === "" ||
        hour === "" ||
        dayOfWeek === "" ||
        holiday === "" ||
        temperature === "" ||
        humidity === "" ||
        squareFootage === "" ||
        occupancy === "" ||
        hvacUsage === "" ||
        lightingUsage === "" ||
        renewableEnergy === ""
    ) {

        showError(
            "Please fill all Energy Prediction inputs."
        );

        return;
    }


    // --------------------------------------------------------
    // VALIDATE HOUR
    // --------------------------------------------------------

    if (
        Number(hour) < 0 ||
        Number(hour) > 23
    ) {

        showError(
            "Hour must be between 0 and 23."
        );

        return;
    }


    // --------------------------------------------------------
    // VALIDATE HUMIDITY
    // --------------------------------------------------------

    if (
        Number(humidity) < 0 ||
        Number(humidity) > 100
    ) {

        showError(
            "Humidity must be between 0% and 100%."
        );

        return;
    }


    // --------------------------------------------------------
    // SHOW LOADING
    // --------------------------------------------------------

    loading.style.display = "block";

    predictButton.disabled = true;

    predictButton.innerHTML =
        '<span class="spinner-border spinner-border-sm me-2"></span>' +
        'Predicting...';


    try {

        // ----------------------------------------------------
        // PREPARE REQUEST DATA
        // ----------------------------------------------------

        const requestData = {

            month: Number(month),

            hour: Number(hour),

            day_of_week: Number(dayOfWeek),

            holiday: holiday,

            temperature: Number(temperature),

            humidity: Number(humidity),

            square_footage: Number(squareFootage),

            occupancy: Number(occupancy),

            hvac_usage: hvacUsage,

            lighting_usage: lightingUsage,

            renewable_energy: Number(renewableEnergy)

        };


        console.log(
            "Energy Prediction Input:",
            requestData
        );


        // ----------------------------------------------------
        // SEND REQUEST TO FLASK
        // ----------------------------------------------------

        const response = await fetch(
            "/api/energy/predict",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(requestData)

            }
        );


        // ----------------------------------------------------
        // READ RESPONSE
        // ----------------------------------------------------

        const data =
            await response.json();


        console.log(
            "Energy Prediction Response:",
            data
        );


        // ----------------------------------------------------
        // HANDLE ERROR RESPONSE
        // ----------------------------------------------------

        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.message ||
                data.error ||
                "Energy prediction failed."
            );

        }


        // ----------------------------------------------------
        // GET PREDICTION
        // ----------------------------------------------------

        const prediction =
            data.prediction;


        if (!prediction) {

            throw new Error(
                "Prediction data was not returned by the server."
            );

        }


        // ----------------------------------------------------
        // SHOW RESULT CARD
        // ----------------------------------------------------

        resultCard.style.display = "block";


        // ----------------------------------------------------
        // ENERGY CONSUMPTION
        // ----------------------------------------------------

        const energyValue =
            Number(
                prediction.energy_consumption
            );


        document.getElementById(
            "energyResult"
        ).textContent =
            isNaN(energyValue)
                ? "--"
                : energyValue.toFixed(2);


        // ----------------------------------------------------
        // DEMAND LEVEL
        // ----------------------------------------------------

        document.getElementById(
            "demandResult"
        ).textContent =
            prediction.demand_level ||
            "--";


        // ----------------------------------------------------
        // RISK LEVEL
        // ----------------------------------------------------

        const riskElement =
            document.getElementById(
                "riskResult"
            );


        const risk =
            prediction.risk_level ||
            "--";


        riskElement.textContent =
            risk;


        // Remove previous risk classes

        riskElement.className =
            "risk-badge";


        // Add corresponding class

        switch (
            risk.toLowerCase()
        ) {

            case "low":

                riskElement.classList.add(
                    "low"
                );

                break;


            case "medium":

                riskElement.classList.add(
                    "medium"
                );

                break;


            case "high":

                riskElement.classList.add(
                    "high"
                );

                break;


            case "critical":

                riskElement.classList.add(
                    "critical"
                );

                break;


            default:

                break;

        }


        // ----------------------------------------------------
        // PREDICTION TYPE
        // ----------------------------------------------------

        document.getElementById(
            "predictionType"
        ).textContent =
            data.prediction_type ||
            "ML";


        // ----------------------------------------------------
        // MODEL NAME
        // ----------------------------------------------------

        document.getElementById(
            "modelResult"
        ).textContent =
            data.model ||
            "Energy Consumption ML Model";


        // ----------------------------------------------------
        // STATUS
        // ----------------------------------------------------

        document.getElementById(
            "statusResult"
        ).textContent =
            "Prediction Successful";


        // ----------------------------------------------------
        // SCROLL TO RESULT
        // ----------------------------------------------------

        resultCard.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });


    }


    catch (error) {

        // ----------------------------------------------------
        // CONSOLE ERROR
        // ----------------------------------------------------

        console.error(
            "Energy Prediction Error:",
            error
        );


        // ----------------------------------------------------
        // SHOW ERROR
        // ----------------------------------------------------

        showError(
            error.message ||
            "Unable to connect to Energy ML API."
        );


        // ----------------------------------------------------
        // UPDATE STATUS
        // ----------------------------------------------------

        document.getElementById(
            "statusResult"
        ).textContent =
            "Prediction Failed";

    }


    finally {

        // ----------------------------------------------------
        // HIDE LOADING
        // ----------------------------------------------------

        loading.style.display = "none";


        // ----------------------------------------------------
        // ENABLE BUTTON
        // ----------------------------------------------------

        predictButton.disabled = false;

        predictButton.innerHTML =
            '<i class="bi bi-cpu-fill me-2"></i>' +
            'Predict Energy Consumption';

    }

});


// ============================================================
// SHOW ERROR FUNCTION
// ============================================================

function showError(message) {

    errorBox.textContent = message;

    errorBox.style.display = "block";

}


// ============================================================
// INITIAL STATE
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        resultCard.style.display = "block";

        document.getElementById(
            "energyResult"
        ).textContent = "--";

        document.getElementById(
            "demandResult"
        ).textContent = "--";

        document.getElementById(
            "riskResult"
        ).textContent = "--";

        document.getElementById(
            "modelResult"
        ).textContent = "--";

        document.getElementById(
            "predictionType"
        ).textContent = "ML";

        document.getElementById(
            "statusResult"
        ).textContent = "Ready";

    }
);