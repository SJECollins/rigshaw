const journeyMap = L.map('journey-map').setView([{{ journey.start_location_lat }}, {{ journey.start_location_long }}], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(journeyMap);

const startMarker = L.marker([{{ journey.start_location_lat }}, {{ journey.start_location_long }}])
    .addTo(journeyMap)
    .bindPopup("<b>Start</b>")
    .openPopup();

const endMarker = L.marker([{{ journey.destination_lat }}, {{ journey.destination_long }}])
    .addTo(journeyMap)
    .bindPopup("<b>End</b>")
    .openPopup();

const routeLine = L.polyline([startMarker.getLatLng(), endMarker.getLatLng()], { color: 'blue' }).addTo(journeyMap);

const meetingMap = L.map('meeting-map').setView([{{ journey.start_location_lat }}, {{ journey.start_location_long }}], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(meetingMap);

document.querySelectorAll('.meeting-location').forEach(function(link) {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const lat = link.getAttribute('data-lat');
        const lng = link.getAttribute('data-lng');

        if (window.meetingMarker) {
            meetingMap.removeLayer(window.meetingMarker);
        }

        window.meetingMarker = L.marker([lat, lng])
            .addTo(meetingMap)
            .bindPopup("<b>Proposed Meeting Location</b>")
            .openPopup();

        meetingMap.panTo([lat, lng]);
    });
});