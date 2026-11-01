// ======================================================
// DASHBOARD CHARTS
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        createTrafficChart();

        createEnergyChart();

        createCityMap();

    }
);


// ======================================================
// TRAFFIC CHART
// ======================================================

function createTrafficChart() {

    const canvas =
        document.getElementById(
            "trafficChart"
        );


    if (!canvas) {
        return;
    }


    new Chart(
        canvas,
        {

            type: "line",

            data: {

                labels: [
                    "8 AM",
                    "9 AM",
                    "10 AM",
                    "11 AM",
                    "12 PM",
                    "1 PM",
                    "2 PM",
                    "3 PM",
                    "4 PM",
                    "5 PM",
                    "6 PM",
                    "7 PM"
                ],

                datasets: [

                    {

                        label:
                            "Actual Traffic",

                        data: [
                            42,
                            51,
                            47,
                            53,
                            49,
                            56,
                            52,
                            58,
                            61,
                            67,
                            72,
                            64
                        ],

                        borderWidth: 2,

                        tension: .4,

                        fill: true,

                        backgroundColor:
                            "rgba(34,211,238,.06)",

                        borderColor:
                            "#22d3ee",

                        pointRadius: 2,

                        pointBackgroundColor:
                            "#22d3ee"

                    },

                    {

                        label:
                            "AI Forecast",

                        data: [
                            null,
                            null,
                            null,
                            null,
                            null,
                            null,
                            null,
                            null,
                            61,
                            69,
                            78,
                            73
                        ],

                        borderWidth: 2,

                        borderDash: [
                            5,
                            5
                        ],

                        tension: .4,

                        borderColor:
                            "#a855f7",

                        pointRadius: 2,

                        pointBackgroundColor:
                            "#a855f7"

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        display: true,

                        labels: {

                            color: "#94a3b8",

                            font: {
                                size: 8
                            },

                            boxWidth: 10

                        }

                    }

                },

                scales: {

                    x: {

                        grid: {
                            display: false
                        },

                        ticks: {

                            color:
                                "#64748b",

                            font: {
                                size: 8
                            }

                        }

                    },

                    y: {

                        beginAtZero: true,

                        grid: {

                            color:
                                "rgba(148,163,184,.06)"

                        },

                        ticks: {

                            color:
                                "#64748b",

                            font: {
                                size: 8
                            }

                        }

                    }

                }

            }

        }
    );

}


// ======================================================
// ENERGY CHART
// ======================================================

function createEnergyChart() {

    const canvas =
        document.getElementById(
            "energyChart"
        );


    if (!canvas) {
        return;
    }


    new Chart(
        canvas,
        {

            type: "line",

            data: {

                labels: [
                    "8 AM",
                    "9 AM",
                    "10 AM",
                    "11 AM",
                    "12 PM",
                    "1 PM",
                    "2 PM",
                    "3 PM",
                    "4 PM",
                    "5 PM",
                    "6 PM",
                    "7 PM"
                ],

                datasets: [

                    {

                        label:
                            "Energy Usage",

                        data: [
                            48,
                            51,
                            53,
                            50,
                            57,
                            61,
                            58,
                            63,
                            67,
                            69,
                            73,
                            71
                        ],

                        borderColor:
                            "#a855f7",

                        backgroundColor:
                            "rgba(168,85,247,.06)",

                        borderWidth: 2,

                        tension: .4,

                        fill: true,

                        pointRadius: 2,

                        pointBackgroundColor:
                            "#a855f7"

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
                    }

                },

                scales: {

                    x: {

                        grid: {
                            display: false
                        },

                        ticks: {

                            color:
                                "#64748b",

                            font: {
                                size: 8
                            }

                        }

                    },

                    y: {

                        beginAtZero: true,

                        grid: {

                            color:
                                "rgba(148,163,184,.06)"

                        },

                        ticks: {

                            color:
                                "#64748b",

                            font: {
                                size: 8
                            }

                        }

                    }

                }

            }

        }
    );

}


// ======================================================
// CITY MAP
// ======================================================
//
// IMPORTANT:
// This map does NOT affect any ML module.
// It is only a visualization layer.
// ======================================================

function createCityMap() {

    const mapElement =
        document.getElementById(
            "cityMap"
        );


    if (!mapElement) {
        return;
    }


    // ------------------------------------------------------
    // Default fallback location
    // ------------------------------------------------------
    //
    // Used only if the browser refuses location access.
    // ------------------------------------------------------

    const fallbackLocation = {

        lat: 16.5449,

        lng: 81.5212

    };


    // ------------------------------------------------------
    // CREATE MAP
    // ------------------------------------------------------

    const map =
        L.map(
            "cityMap",
            {
                zoomControl: false
            }
        );


    // ------------------------------------------------------
    // OPEN STREET MAP
    // ------------------------------------------------------

    L.tileLayer(

        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

        {

            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',

            maxZoom: 19

        }

    ).addTo(map);


    // ------------------------------------------------------
    // STATUS COLORS
    // ------------------------------------------------------

    const colors = {

        central: "#22d3ee",

        normal: "#34d399",

        warning: "#f59e0b",

        critical: "#fb4b5d"

    };


    // ------------------------------------------------------
    // CREATE ZONE MARKERS
    // ------------------------------------------------------

    function createZones(
        centerLat,
        centerLng
    ) {

        const zones = [

            {
                label:
                    "Central Zone",

                type:
                    "City Center",

                status:
                    "normal",

                lat:
                    centerLat,

                lng:
                    centerLng
            },


            {
                label:
                    "Residential Zone",

                type:
                    "Residential Monitoring",

                status:
                    "normal",

                lat:
                    centerLat + 0.0060,

                lng:
                    centerLng + 0.0040
            },


            {
                label:
                    "Commercial Zone",

                type:
                    "Commercial Monitoring",

                status:
                    "warning",

                lat:
                    centerLat - 0.0050,

                lng:
                    centerLng + 0.0055
            },


            {
                label:
                    "Danger Zone",

                type:
                    "High Risk Monitoring",

                status:
                    "critical",

                lat:
                    centerLat + 0.0025,

                lng:
                    centerLng - 0.0070
            }

        ];


        zones.forEach(
            function (zone) {


                const zoneColor =
                    zone.label ===
                    "Central Zone"

                        ? colors.central

                        : colors[
                            zone.status
                        ];


                // ------------------------------------------------
                // ZONE AREA
                // ------------------------------------------------

                const zoneArea =
                    L.circle(

                        [
                            zone.lat,
                            zone.lng
                        ],

                        {

                            radius:
                                zone.label ===
                                "Central Zone"
                                    ? 750
                                    : 600,

                            color:
                                zoneColor,

                            fillColor:
                                zoneColor,

                            fillOpacity:
                                zone.status ===
                                "critical"
                                    ? 0.22
                                    : 0.12,

                            weight: 2

                        }

                    ).addTo(map);


                // ------------------------------------------------
                // ZONE MARKER
                // ------------------------------------------------

                const marker =
                    L.circleMarker(

                        [
                            zone.lat,
                            zone.lng
                        ],

                        {

                            radius: 8,

                            color:
                                "#ffffff",

                            weight: 2,

                            fillColor:
                                zoneColor,

                            fillOpacity:
                                0.95

                        }

                    ).addTo(map);


                // ------------------------------------------------
                // POPUP
                // ------------------------------------------------

                marker.bindPopup(`

                    <div style="
                        font-family:Arial;
                        min-width:160px;
                    ">

                        <strong style="
                            font-size:13px;
                            color:#111827;
                        ">
                            ${zone.label}
                        </strong>

                        <br><br>

                        <span style="
                            color:#6b7280;
                        ">
                            Type:
                        </span>

                        ${zone.type}

                        <br>

                        <span style="
                            color:#6b7280;
                        ">
                            Status:
                        </span>

                        <strong>
                            ${zone.status.toUpperCase()}
                        </strong>

                    </div>

                `);


                // ------------------------------------------------
                // TEXT LABEL
                // ------------------------------------------------

                L.marker(

                    [
                        zone.lat,
                        zone.lng
                    ],

                    {

                        icon:
                            L.divIcon({

                                className:
                                    "dashboard-zone-label",

                                html: `

                                    <div style="
                                        background:rgba(5,9,20,.88);
                                        border:1px solid ${zoneColor};
                                        color:white;
                                        padding:4px 7px;
                                        border-radius:6px;
                                        font-size:8px;
                                        font-weight:700;
                                        white-space:nowrap;
                                        box-shadow:
                                            0 4px 14px
                                            rgba(0,0,0,.30);
                                    ">

                                        ${zone.label}

                                    </div>

                                `,

                                iconSize:
                                    null,

                                iconAnchor:
                                    [-8, 28]

                            }),

                        interactive:
                            false

                    }

                ).addTo(map);

            }
        );

    }


    // ------------------------------------------------------
    // CURRENT LOCATION
    // ------------------------------------------------------

    function showCurrentLocation(
        latitude,
        longitude
    ) {

        map.setView(
            [
                latitude,
                longitude
            ],
            14
        );


        // --------------------------------------------------
        // YOU ARE HERE MARKER
        // --------------------------------------------------

        const userMarker =
            L.circleMarker(

                [
                    latitude,
                    longitude
                ],

                {

                    radius: 9,

                    color:
                        "#ffffff",

                    weight: 3,

                    fillColor:
                        "#2563eb",

                    fillOpacity:
                        1

                }

            ).addTo(map);


        userMarker.bindPopup(`

            <div style="
                font-family:Arial;
                min-width:150px;
            ">

                <strong style="
                    font-size:13px;
                    color:#111827;
                ">
                    📍 You Are Here
                </strong>

                <br><br>

                <span style="
                    color:#6b7280;
                ">
                    Current device location
                </span>

            </div>

        `);


        // --------------------------------------------------
        // ACCURACY CIRCLE
        // --------------------------------------------------

        L.circle(

            [
                latitude,
                longitude
            ],

            {

                radius: 80,

                color:
                    "#2563eb",

                fillColor:
                    "#2563eb",

                fillOpacity:
                    0.08,

                weight: 1

            }

        ).addTo(map);


        // --------------------------------------------------
        // CREATE PROJECT ZONES
        // --------------------------------------------------

        createZones(
            latitude,
            longitude
        );

    }


    // ------------------------------------------------------
    // GEOLOCATION ERROR
    // ------------------------------------------------------

    function useFallbackLocation() {

        showCurrentLocation(

            fallbackLocation.lat,

            fallbackLocation.lng

        );

    }


    // ------------------------------------------------------
    // GET CURRENT LOCATION
    // ------------------------------------------------------

    if (
        "geolocation"
        in navigator
    ) {

        navigator.geolocation.getCurrentPosition(

            function (position) {

                const latitude =
                    position.coords.latitude;

                const longitude =
                    position.coords.longitude;


                showCurrentLocation(
                    latitude,
                    longitude
                );

            },

            function (error) {

                console.warn(
                    "Location access failed:",
                    error.message
                );


                useFallbackLocation();

            },

            {

                enableHighAccuracy:
                    true,

                timeout:
                    15000,

                maximumAge:
                    30000

            }

        );

    } else {

        console.warn(
            "Geolocation is not supported by this browser."
        );


        useFallbackLocation();

    }


    // ------------------------------------------------------
    // ZOOM CONTROL
    // ------------------------------------------------------

    L.control.zoom({

        position:
            "bottomright"

    }).addTo(map);

}