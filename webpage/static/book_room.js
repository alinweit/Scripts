function openPopUp(button) {
    var popup = button.nextElementSibling;
    popup.style.display = "block";
}

function closePopUp(button) {
    var popup = button.parentElement;
    popup.style.display = "none";
}

function book(button) {
  var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  var userID = button.getAttribute("data-user-id");
  var raumNR = button.getAttribute("data-raum-nr");
  var datum = button.getAttribute("data-datum");
  var data = `${userID}|${raumNR}|${datum}`

  $.ajax({
      type: "GET",
      url: `/make_booking/${data}/`,
      success: function (response) {
          alert("Der Angleich war erfolgreich!");
      },
      error: function (xhr, status, error) {
          console.log("Fehler bei der AJAX-Anfrage:", error);
      }
  });
}