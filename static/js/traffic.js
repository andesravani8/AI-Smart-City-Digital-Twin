document.addEventListener("DOMContentLoaded", function () {

    // ============================================================
    // GET FORM
    // ============================================================

    const trafficForm =
        document.getElementById("trafficForm");

    if (!trafficForm) {
        console.error("Traffic form not found.");
        return;
    }


    // ============================================================
    // FORM SUBMIT
    // ============================================================

    trafficForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            // ====================================================
            // GET INPUT ELEMENTS
            // ====================================================

            const junctionElement =
                document.getElementById("junction");

            const currentVehiclesElement =
                document.getElementById("currentVehicles");

            const hourElement =
                document.getElementById("hour");

            const dayElement =
                document.getElementById("day");

            const monthElement =
                document.getElementById("month");

            const dayOfWeekElement =
                document.getElementById("dayOfWeek");

            const isWeekendElement =
                document.getElementById("isWeekend");


            // ====================================================
            // CONVERT VALUES TO NUMBERS
            // ====================================================

            const junction =
                Number(junctionElement.value);

            const currentVehicles =
                Number(currentVehiclesElement.value);

            const hour =
                Number(hourElement.value);

            const day =
                Number(dayElement.value);

            const month =
                Number(monthElement.value);

            const dayOfWeek =
                Number(dayOfWeekElement.value);

            const isWeekend =
                Number(isWeekendElement.value);


            // ====================================================
            // GET UI ELEMENTS
            // ====================================================

            const button =
                document.getElementById(
                    "predictTrafficBtn"
                );

            const loading =
                document.getElementById(
                    "trafficLoading"
                );

            const errorBox =
                document.getElementById(
                    "trafficError"
                );

            const resultBox =
                document.getElementById(
                    "trafficResult"
                );

            const abnormalBox =
                document.getElementById(
                    "abnormalTraffic"
                );


            // ====================================================
            // HIDE PREVIOUS MESSAGES
            // ====================================================

            if (errorBox) {

                errorBox.style.display =
                    "none";

                errorBox.textContent =
                    "";
            }


            if (resultBox) {

                resultBox.style.display =
                    "none";
            }


            if (abnormalBox) {

                abnormalBox.style.display =
                    "none";
            }


            // ====================================================
            // VALIDATION
            // ====================================================

            if (
                !Number.isInteger(junction) ||
                junction < 1 ||
                junction > 4
            ) {

                showError(
                    "Please select a valid junction."
                );

                return;
            }


            if (
                !Number.isFinite(currentVehicles) ||
                currentVehicles < 0
            ) {

                showError(
                    "Please enter a valid current vehicle count."
                );

                return;
            }


            if (
                !Number.isInteger(hour) ||
                hour < 0 ||
                hour > 23
            ) {

                showError(
                    "Hour must be between 0 and 23."
                );

                return;
            }


            if (
                !Number.isInteger(day) ||
                day < 1 ||
                day > 31
            ) {

                showError(
                    "Day must be between 1 and 31."
                );

                return;
            }


            if (
                !Number.isInteger(month) ||
                month < 1 ||
                month > 12
            ) {

                showError(
                    "Please select a valid month."
                );

                return;
            }


            if (
                !Number.isInteger(dayOfWeek) ||
                dayOfWeek < 0 ||
                dayOfWeek > 6
            ) {

                showError(
                    "Please select a valid day of week."
                );

                return;
            }


            if (
                isWeekend !== 0 &&
                isWeekend !== 1
            ) {

                showError(
                    "Weekend value must be No or Yes."
                );

                return;
            }


            // ====================================================
            // DEBUG INPUT
            // ====================================================

            console.log(
                "========== TRAFFIC INPUT =========="
            );

            console.log(
                "Junction:",
                junction
            );

            console.log(
                "Current Vehicles:",
                currentVehicles
            );

            console.log(
                "Hour:",
                hour
            );

            console.log(
                "Day:",
                day
            );

            console.log(
                "Month:",
                month
            );

            console.log(
                "Day Of Week:",
                dayOfWeek
            );

            console.log(
                "Weekend:",
                isWeekend
            );


            // ====================================================
            // LOADING STATE
            // ====================================================

            if (button) {

                button.disabled =
                    true;

                button.innerHTML =
                    '<i class="bi bi-arrow-repeat me-2"></i> Predicting...';
            }


            if (loading) {

                loading.style.display =
                    "block";
            }


            // ====================================================
            // DATA FOR FLASK
            // ====================================================
            //
            // IMPORTANT:
            // These names MUST match traffic.py
            // ====================================================

            const requestData = {

                junction: junction,

                hour: hour,

                day: day,

                month: month,

                day_of_week: dayOfWeek,

                is_weekend: isWeekend,

                current_vehicles:
                    currentVehicles

            };


            console.log(
                "Traffic API Request:",
                requestData
            );


            // ====================================================
            // CALL FLASK API
            // ====================================================

            try {

                const response =
                    await fetch(
                        "/api/traffic/predict",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    requestData
                                )
                        }
                    );


                // =================================================
                // READ RESPONSE
                // =================================================

                const data =
                    await response.json();


                console.log(
                    "Traffic API Response:",
                    data
                );


                // =================================================
                // API ERROR
                // =================================================

                if (
                    !response.ok ||
                    !data.success
                ) {

                    showError(
                        data.error ||
                        data.message ||
                        "Traffic ML prediction failed."
                    );

                    return;
                }


                // =================================================
                // PREDICTED VEHICLES
                // =================================================

                const predictedVehicles =
                    Number(
                        data.predicted_vehicles
                    );


                if (
                    !Number.isFinite(
                        predictedVehicles
                    )
                ) {

                    showError(
                        "Invalid prediction returned by ML model."
                    );

                    return;
                }


                // =================================================
                // DEVIATION
                // =================================================

                let deviation = 0;


                if (
                    data.deviation_percentage !==
                    null &&
                    data.deviation_percentage !==
                    undefined
                ) {

                    deviation =
                        Number(
                            data.deviation_percentage
                        );

                } else if (
                    predictedVehicles > 0
                ) {

                    deviation =
                        (
                            (
                                currentVehicles -
                                predictedVehicles
                            ) /
                            predictedVehicles
                        ) * 100;
                }


                if (
                    !Number.isFinite(
                        deviation
                    )
                ) {

                    deviation = 0;
                }


                // =================================================
                // CONGESTION
                // =================================================

                const congestion =
                    data.congestion ||
                    "Unknown";


                // =================================================
                // RISK
                // =================================================

                const risk =
                    data.risk ||
                    "Unknown";


                // =================================================
                // DISPLAY PREDICTED VEHICLES
                // =================================================

                const predictedElement =
                    document.getElementById(
                        "predictedVehicles"
                    );


                if (predictedElement) {

                    predictedElement.textContent =
                        predictedVehicles.toFixed(1);
                }


                // =================================================
                // DISPLAY CURRENT VEHICLES
                // =================================================

                const currentElement =
                    document.getElementById(
                        "currentVehicleResult"
                    );


                if (currentElement) {

                    currentElement.textContent =
                        currentVehicles.toFixed(0);
                }


                // =================================================
                // DISPLAY DEVIATION
                // =================================================

                const deviationElement =
                    document.getElementById(
                        "trafficDeviation"
                    );


                if (deviationElement) {

                    deviationElement.textContent =
                        `${deviation >= 0 ? "+" : ""}${deviation.toFixed(1)}%`;
                }


                // =================================================
                // DISPLAY CONGESTION
                // =================================================

                const congestionElement =
                    document.getElementById(
                        "trafficCongestion"
                    );


                if (congestionElement) {

                    congestionElement.textContent =
                        congestion;
                }


                // =================================================
                // DISPLAY RISK
                // =================================================

                const riskElement =
                    document.getElementById(
                        "trafficRisk"
                    );


                if (riskElement) {

                    riskElement.textContent =
                        risk;


                    // Remove previous classes
                    riskElement.classList.remove(
                        "low",
                        "medium",
                        "high",
                        "critical"
                    );


                    const riskValue =
                        String(risk)
                            .toLowerCase();


                    if (
                        riskValue === "low"
                    ) {

                        riskElement.classList.add(
                            "low"
                        );

                    } else if (
                        riskValue === "medium"
                    ) {

                        riskElement.classList.add(
                            "medium"
                        );

                    } else if (
                        riskValue === "high"
                    ) {

                        riskElement.classList.add(
                            "high"
                        );

                    } else if (
                        riskValue === "critical"
                    ) {

                        riskElement.classList.add(
                            "critical"
                        );
                    }
                }


                // =================================================
                // PREDICTION TYPE
                // =================================================

                const predictionTypeElement =
                    document.getElementById(
                        "predictionType"
                    );


                if (predictionTypeElement) {

                    predictionTypeElement.textContent =
                        data.prediction_type ||
                        "ML";
                }


                // =================================================
                // ABNORMAL TRAFFIC
                // =================================================

                const abnormalTraffic =
                    data.abnormal_traffic === true ||
                    deviation >= 30;


                if (abnormalBox) {

                    if (abnormalTraffic) {

                        abnormalBox.style.display =
                            "block";

                    } else {

                        abnormalBox.style.display =
                            "none";
                    }
                }


                // =================================================
                // SHOW RESULT
                // =================================================

                if (resultBox) {

                    resultBox.style.display =
                        "block";
                }


                console.log(
                    "Traffic prediction successful."
                );


            } catch (error) {

                // =================================================
                // CONNECTION ERROR
                // =================================================

                console.error(
                    "Traffic API Error:",
                    error
                );


                showError(
                    "Unable to connect to the Traffic ML API."
                );


            } finally {

                // =================================================
                // RESTORE BUTTON
                // =================================================

                if (loading) {

                    loading.style.display =
                        "none";
                }


                if (button) {

                    button.disabled =
                        false;

                    button.innerHTML =
                        '<i class="bi bi-cpu-fill me-2"></i> Predict Traffic';
                }

            }

        }
    );


    // ============================================================
    // ERROR FUNCTION
    // ============================================================

    function showError(message) {

        const errorBox =
            document.getElementById(
                "trafficError"
            );


        if (!errorBox) {

            alert(message);

            return;
        }


        errorBox.textContent =
            message;


        errorBox.style.display =
            "block";
    }

});