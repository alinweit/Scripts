document.addEventListener('DOMContentLoaded', function () {
    var bookingsToDelete = [];
    var checkboxes = document.querySelectorAll('input[name="selected_bookings"]');

    var removeButton = document.getElementById('removeSelectedBookings');
    removeButton.addEventListener('click', function() {
        selectedEntries();
        removeBooking();
    });

    function selectedEntries() {   
    bookingsToDelete = [];     
        checkboxes.forEach(function (checkbox) {
            if (checkbox.checked) {
                var bookingId = checkbox.value;
                bookingsToDelete.push(bookingId);
            }
        });
    }

    function removeBooking() {
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        listToDelete = bookingsToDelete.toString();
    
        $.ajax({
            type: "GET",
            url: `/remove_bookings/${listToDelete}/`,
            success: function () {
                location.reload();
            }
        });
    }
});