document
  .getElementById("add-meeting-checkbox")
  .addEventListener("change", function () {
    const meetingForm = document.getElementById("meeting-form");
    const isChecked = this.checked;

    meetingForm.style.display = isChecked ? "block" : "none";

    if (isChecked) {
      document
        .getElementById("id_meeting_location_lat")
        .setAttribute("required", true);
      document
        .getElementById("id_meeting_location_long")
        .setAttribute("required", true);
      document.getElementById("id_meeting_time").setAttribute("required", true);
    } else {
      document
        .getElementById("id_meeting_location_lat")
        .removeAttribute("required");
      document
        .getElementById("id_meeting_location_long")
        .removeAttribute("required");
      document.getElementById("id_meeting_time").removeAttribute("required");
    }
  });

let startMarker, endMarker, routeLine, meetingMarker;

map.on("click", function (e) {
  const clickedCoords = e.latlng;

  const addMeeting = document.getElementById("add-meeting-checkbox").checked;

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
  } else if (addMeeting && !meetingMarker) {
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

  if (meetingMarker) {
    map.removeLayer(meetingMarker);
    meetingMarker = null;
  }

  document.getElementById("id_start_location_lat").value = "";
  document.getElementById("id_start_location_long").value = "";
  document.getElementById("id_destination_lat").value = "";
  document.getElementById("id_destination_long").value = "";
  document.getElementById("id_meeting_location_lat").value = "";
  document.getElementById("id_meeting_location_long").value = "";
});
