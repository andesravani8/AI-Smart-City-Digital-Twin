document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("weatherForm");

    if (!form) {
        return;
    }


    // =====================================================
    // ELEMENTS
    // =====================================================

    const loading =
        document.getElementById("weatherLoading");

    const errorBox =
        document.getElementById("weatherError");

    const resultCard =
        document.getElementById("weatherResult");

    const temperatureResult =
        document.getElementById("temperatureResult");

    const temperatureLevel =
        document.getElementById("temperatureLevel");

    const weatherRisk =
        document.getElementById("weatherRisk");

    const weatherModel =
        document.getElementById("weatherModel");


    // =====================================================
    // FORM SUBMIT
    // =====================================================

    form.addEventListener("submit", async function (event) {

        event.preventDefault();


        // =================================================
        // VISIBLE INPUT VALUES
        // =================================================

        const year =
            document.getElementById("year").value;

        const month =
            document.getElementById("month").value;

        const day =
            document.getElementById("day").value;

        const hour =
            document.getElementById("hour").value;

        const dayOfWeek =
            document.getElementById("day_of_week").value;


        const pressure =
            document.getElementById("pressure").value;

        const humidity =
            document.getElementById("humidity").value;

        const windspeed =
            document.getElementById("windspeed").value;

        const windDirection =
            document.getElementById("wind_direction").value;


        // =================================================
        // BASIC VALIDATION
        // =================================================

        if (
            year === "" ||
            month === "" ||
            day === "" ||
            hour === "" ||
            dayOfWeek === "" ||
            pressure === "" ||
            humidity === "" ||
            windspeed === "" ||
            windDirection === ""
        ) {

            errorBox.textContent =
                "Please fill all required weather inputs.";

            errorBox.style.display = "block";

            return;
        }


        const numericHumidity = Number(humidity);
        const numericHour = Number(hour);
        const numericMonth = Number(month);
        const numericDay = Number(day);
        const numericWindDirection = Number(windDirection);
        const numericWindSpeed = Number(windspeed);


        if (
            numericHumidity < 0 ||
            numericHumidity > 100
        ) {

            errorBox.textContent =
                "Humidity must be between 0 and 100.";

            errorBox.style.display = "block";

            return;
        }


        if (
            numericHour < 0 ||
            numericHour > 23
        ) {

            errorBox.textContent =
                "Hour must be between 0 and 23.";

            errorBox.style.display = "block";

            return;
        }


        if (
            numericMonth < 1 ||
            numericMonth > 12
        ) {

            errorBox.textContent =
                "Month must be between 1 and 12.";

            errorBox.style.display = "block";

            return;
        }


        if (
            numericDay < 1 ||
            numericDay > 31
        ) {

            errorBox.textContent =
                "Day must be between 1 and 31.";

            errorBox.style.display = "block";

            return;
        }


        if (numericWindSpeed < 0) {

            errorBox.textContent =
                "Wind speed cannot be negative.";

            errorBox.style.display = "block";

            return;
        }


        if (
            numericWindDirection < 0 ||
            numericWindDirection > 360
        ) {

            errorBox.textContent =
                "Wind direction must be between 0 and 360.";

            errorBox.style.display = "block";

            return;
        }


        // =================================================
        // HIDE PREVIOUS ERROR / RESULT
        // =================================================

        loading.style.display = "flex";

        errorBox.style.display = "none";

        resultCard.style.display = "none";


        try {

            // =================================================
            // DEFAULT VALUES FOR HIDDEN ML FEATURES
            // =================================================
            //
            // These values were already used as examples
            // in the original Weather UI.
            //
            // They are hidden from the user only to make
            // the interface simpler.
            // =================================================

            const tpot = 285.0;

            const tdew = 10.0;

            const vpmax = 12.0;

            const vpact = 8.0;

            const vpdef = 4.0;

            const specificHumidity = 6.0;

            const h2oc = 10.0;

            const density = 1200.0;

            const maxWindspeed = 5.0;


            // =================================================
            // API REQUEST
            // =================================================

            const response = await fetch(
                "/api/weather/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        // Visible values
                        pressure: Number(pressure),

                        humidity: Number(humidity),

                        windspeed: Number(windspeed),

                        wind_direction: Number(windDirection),

                        year: Number(year),

                        month: Number(month),

                        day: Number(day),

                        hour: Number(hour),

                        day_of_week: Number(dayOfWeek),


                        // Hidden ML values
                        tpot: tpot,

                        tdew: tdew,

                        vpmax: vpmax,

                        vpact: vpact,

                        vpdef: vpdef,

                        specific_humidity: specificHumidity,

                        h2oc: h2oc,

                        density: density,

                        max_windspeed: maxWindspeed

                    })
                }
            );


            // =================================================
            // READ RESPONSE
            // =================================================

            const data =
                await response.json();


            if (
                !response.ok ||
                !data.success
            ) {

                throw new Error(
                    data.message ||
                    data.error ||
                    "Weather prediction failed."
                );

            }


            // =================================================
            // GET PREDICTION
            // =================================================

            const prediction =
                data.prediction;


            const predictedTemperature =
                prediction?.temperature ??
                prediction?.predicted_temperature ??
                prediction?.temperature_prediction ??
                data.temperature ??
                data.predicted_temperature ??
                "--";


            // =================================================
            // VALIDATE RESULT
            // =================================================

            const temp =
                Number(predictedTemperature);


            if (!Number.isFinite(temp)) {

                throw new Error(
                    "Invalid temperature prediction received from server."
                );

            }


            // =================================================
            // SHOW RESULT
            // =================================================

            resultCard.style.display = "block";


            temperatureResult.textContent =
                temp.toFixed(2);


            // =================================================
            // TEMPERATURE LEVEL
            // =================================================

            let level = "";


            if (temp < 15) {

                level = "Cold";

            }
            else if (temp < 25) {

                level = "Cool";

            }
            else if (temp < 32) {

                level = "Moderate";

            }
            else if (temp < 38) {

                level = "Hot";

            }
            else {

                level = "Very Hot";

            }


            temperatureLevel.textContent =
                prediction?.temperature_level ||
                level;


            // =================================================
            // WEATHER RISK
            // =================================================

            let risk = "";


            if (temp < 25) {

                risk = "Low";

            }
            else if (temp < 32) {

                risk = "Medium";

            }
            else if (temp < 38) {

                risk = "High";

            }
            else {

                risk = "Critical";

            }


            weatherRisk.textContent =
                prediction?.risk_level ||
                risk;


            // =================================================
            // MODEL
            // =================================================

            weatherModel.textContent =
                data.model ||
                "Weather Temperature ML Model";


        }
        catch (error) {

            console.error(
                "Weather prediction error:",
                error
            );


            errorBox.textContent =
                error.message ||
                "Unable to predict temperature.";


            errorBox.style.display =
                "block";

        }
        finally {

            loading.style.display =
                "none";

        }

    });

});