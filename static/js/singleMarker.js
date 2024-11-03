let meetingMarker;
map.on("click", function (e) {
  const clickedCoords = e.latlng;

  if (!meetingMarker) {
    meetingMarker = L.marker(clickedCoords)
      .addTo(map)
      .bindPopup("<b>Meeting</b>")
      .openPopup();
    document.getElementById("id_meeting_location_lat").value =
      clickedCoords.lat;
    document.getElementById("id_meeting_location_long").value =
      clickedCoords.lng;
  }
});

document.getElementById("clear").addEventListener("click", function () {
  if (meetingMarker) {
    map.removeLayer(meetingMarker);
    meetingMarker = null;
  }
});
