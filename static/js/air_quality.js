// air_quality.js
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("airQualityForm");

    const loading = document.getElementById("loading");

    const errorBox = document.getElementById("errorBox");

    const resultCard = document.getElementById("resultCard");


    form.addEventListener("submit", async function (event) {

        event.preventDefault();


        loading.style.display = "block";

        errorBox.style.display = "none";

        resultCard.style.display = "none";


        try {

            // -----------------------------------------
            // GET INPUT VALUES
            // -----------------------------------------

            const requestData = {

                city: document.getElementById("city").value,

                pm25: Number(
                    document.getElementById("pm25").value
                ),

                pm10: Number(
                    document.getElementById("pm10").value
                ),

                no: Number(
                    document.getElementById("no").value
                ),

                no2: Number(
                    document.getElementById("no2").value
                ),

                nox: Number(
                    document.getElementById("nox").value
                ),

                nh3: Number(
                    document.getElementById("nh3").value
                ),

                co: Number(
                    document.getElementById("co").value
                ),

                so2: Number(
                    document.getElementById("so2").value
                ),

                o3: Number(
                    document.getElementById("o3").value
                ),

                benzene: Number(
                    document.getElementById("benzene").value
                ),

                toluene: Number(
                    document.getElementById("toluene").value
                ),

                xylene: Number(
                    document.getElementById("xylene").value
                ),

                year: Number(
                    document.getElementById("year").value
                ),

                month: Number(
                    document.getElementById("month").value
                ),

                day: Number(
                    document.getElementById("day").value
                )

            };


            // -----------------------------------------
            // SEND DATA TO FLASK
            // -----------------------------------------

            const response = await fetch(
                "/api/air-quality/predict",
                {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(requestData)

                }
            );


            const data = await response.json();


            // -----------------------------------------
            // ERROR HANDLING
            // -----------------------------------------

            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "Air Quality ML prediction failed"
                );

            }


            // -----------------------------------------
            // SHOW RESULT
            // -----------------------------------------

            resultCard.style.display = "block";


            document.getElementById(
                "aqiResult"
            ).textContent =
                data.prediction.aqi;


            document.getElementById(
                "categoryResult"
            ).textContent =
                data.prediction.category;


            const riskElement =
                document.getElementById("riskResult");


            riskElement.textContent =
                data.prediction.risk_level;


            riskElement.className =
                "risk-badge " +
                data.prediction.risk_level.toLowerCase();


            document.getElementById(
                "modelResult"
            ).textContent =
                data.model;


        }


        catch (error) {

            console.error(
                "Air Quality Error:",
                error
            );


            errorBox.textContent =
                error.message;


            errorBox.style.display =
                "block";

        }


        finally {

            loading.style.display =
                "none";

        }

    });

});