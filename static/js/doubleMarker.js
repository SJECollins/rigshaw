let startMarker, endMarker, routeLine;

map.on("click", function (e) {
  const clickedCoords = e.latlng;

  if (!startMarker) {
    startMarker = L.marker(clickedCoords)
      .addTo(map)
      .bindPopup("<b>Start</b>")
      .openPopup();
    document.getElementById("id_start_location_lat").value = clickedCoords.lat;
    document.getElementById("id_start_location_long").value = clickedCoords.lng;
  } else if (!endMarker) {
    endMarker = L.marker(clickedCoords)
      .addTo(map)
      .bindPopup("<b>End</b>")
      .openPopup();
    document.getElementById("id_destination_lat").value = clickedCoords.lat;
    document.getElementById("id_destination_long").value = clickedCoords.lng;

    routeLine = L.polyline([startMarker.getLatLng(), endMarker.getLatLng()], {
      color: "blue",
    }).addTo(map);
  }
});

document.getElementById("clear").addEventListener("click", function () {
  if (startMarker) {
    map.removeLayer(startMarker);
    startMarker = null;
  }

  if (endMarker) {
    map.removeLayer(endMarker);
    endMarker = null;
  }

  if (routeLine) {
    map.removeLayer(routeLine);
    routeLine = null;
  }
});
