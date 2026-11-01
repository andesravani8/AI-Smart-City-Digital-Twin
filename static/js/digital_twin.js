document.addEventListener("DOMContentLoaded", async () => {
    const zonesEl = document.getElementById("zones");
    const infraEl = document.getElementById("infra");
    const totalZonesEl = document.getElementById("totalZones");
    const criticalZonesEl = document.getElementById("criticalZones");
    const totalInfraEl = document.getElementById("totalInfra");

    const statusColors = {
        normal: "#34d399",
        warning: "#fbbf24",
        critical: "#fb7185"
    };

    const zoneRadii = {
        central: 850,
        residential: 1150,
        commercial: 850,
        industrial: 1050,
        danger: 1050
    };

    const typeNames = {
        central: "Central Zone",
        residential: "Residential Zone",
        commercial: "Commercial Zone",
        industrial: "Industrial / Danger Zone",
        danger: "Danger Zone"
    };

    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function zoneStatus(zone) {
        return String(zone.status || "normal").toLowerCase();
    }

    function zoneType(zone) {
        return String(zone.zone_type || "zone").toLowerCase();
    }

    function colorForZone(zone) {
        if (zoneType(zone) === "central") return "#60a5fa";
        return statusColors[zoneStatus(zone)] || "#34d399";
    }

    function radiusForZone(zone) {
        return zoneRadii[zoneType(zone)] || 900;
    }

    function renderZoneList(zones, map) {
        if (!zones.length) {
            zonesEl.innerHTML = '<div class="status-panel">No zones found. Run the supplied database/schema.sql once.</div>';
            return;
        }

        zonesEl.innerHTML = zones.map(zone => {
            const status = zoneStatus(zone);
            const type = zoneType(zone);
            const name = zone.zone_name || zone.zone_code || "Unnamed Zone";
            return `
                <div class="zone-card" data-zone-id="${escapeHtml(zone.id)}">
                    <div class="zone-top">
                        <div>
                            <div class="zone-name">${escapeHtml(name)}</div>
                            <div class="zone-type">${escapeHtml(typeNames[type] || type)}</div>
                        </div>
                        <span class="zone-status-badge status-${escapeHtml(status)}">${escapeHtml(status)}</span>
                    </div>
                </div>`;
        }).join("");

        zonesEl.querySelectorAll(".zone-card").forEach(card => {
            card.addEventListener("click", () => {
                const zone = zones.find(item => String(item.id) === card.dataset.zoneId);
                if (!zone || !zone.latitude || !zone.longitude) return;
                zonesEl.querySelectorAll(".zone-card").forEach(c => c.classList.remove("active"));
                card.classList.add("active");
                map.setView([Number(zone.latitude), Number(zone.longitude)], 14, { animate: true });
                if (zone._marker) zone._marker.openPopup();
            });
        });
    }

    function renderInfrastructure(infrastructure) {
        if (!infrastructure.length) {
            infraEl.innerHTML = '<div class="status-panel">No infrastructure records found.</div>';
            return;
        }

        infraEl.innerHTML = infrastructure.map(item => `
            <div class="infra-row">
                <span>${escapeHtml(item.name)}</span>
                <span class="infra-type">${escapeHtml(item.type || item.status || "asset")}</span>
            </div>
        `).join("");
    }

    try {
        const response = await fetch("/api/digital-twin/", { cache: "no-store" });
        const payload = await response.json();
        if (!response.ok || !payload.success) {
            throw new Error(payload.message || "Digital Twin data unavailable.");
        }

        const data = payload.data || {};
        const zones = data.zones || [];
        const infrastructure = data.infrastructure || [];

        totalZonesEl.textContent = zones.length;
        criticalZonesEl.textContent = zones.filter(z => zoneStatus(z) === "critical").length;
        totalInfraEl.textContent = infrastructure.length;

        const firstValid = zones.find(z => Number.isFinite(Number(z.latitude)) && Number.isFinite(Number(z.longitude)));
        const defaultCenter = firstValid
            ? [Number(firstValid.latitude), Number(firstValid.longitude)]
            : [16.5062, 80.6480];

        const map = L.map("twinMap", { zoomControl: true }).setView(defaultCenter, 13);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution: "© OpenStreetMap contributors"
        }).addTo(map);

        const zoneLayers = [];

        zones.forEach(zone => {
            const lat = Number(zone.latitude);
            const lng = Number(zone.longitude);
            if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;

            const color = colorForZone(zone);
            const type = zoneType(zone);
            const status = zoneStatus(zone);
            const name = zone.zone_name || zone.zone_code || "Zone";

            const circle = L.circle([lat, lng], {
                radius: radiusForZone(zone),
                color,
                weight: 2,
                opacity: .9,
                fillColor: color,
                fillOpacity: type === "central" ? .13 : .18
            }).addTo(map);

            const marker = L.marker([lat, lng], {
                icon: L.divIcon({
                    className: "zone-label-wrap",
                    html: `<div class="zone-label">${escapeHtml(name)}</div>`,
                    iconSize: null,
                    iconAnchor: [0, 15]
                })
            }).addTo(map);

            marker.bindPopup(`
                <div class="zone-popup">
                    <h6>${escapeHtml(name)}</h6>
                    <p>${escapeHtml(typeNames[type] || type)}</p>
                    <p>Status: <span class="zone-status" style="color:${color}">${escapeHtml(status)}</span></p>
                    <p>Zone code: ${escapeHtml(zone.zone_code || "-")}</p>
                </div>
            `);

            zone._marker = marker;
            zoneLayers.push(circle);
        });

        infrastructure.forEach(item => {
            const lat = Number(item.latitude);
            const lng = Number(item.longitude);
            if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;

            L.circleMarker([lat, lng], {
                radius: 5,
                color: "#22d3ee",
                weight: 2,
                fillColor: "#22d3ee",
                fillOpacity: .85
            }).addTo(map).bindPopup(`
                <b>${escapeHtml(item.name)}</b><br>
                ${escapeHtml(item.type || "Infrastructure")}<br>
                Status: ${escapeHtml(item.status || "unknown")}
            `);
        });

        if (zoneLayers.length > 1) {
            const bounds = L.featureGroup(zoneLayers).getBounds().pad(0.18);
            map.fitBounds(bounds, { maxZoom: 14 });
        }

        renderZoneList(zones, map);
        renderInfrastructure(infrastructure);
    } catch (error) {
        zonesEl.innerHTML = `<div class="error-box" style="display:block">${escapeHtml(error.message)}</div>`;
        infraEl.innerHTML = '<div class="error-box" style="display:block">Unable to load infrastructure.</div>';
        totalZonesEl.textContent = "—";
        criticalZonesEl.textContent = "—";
        totalInfraEl.textContent = "—";
    }
});
