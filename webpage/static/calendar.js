document.addEventListener('DOMContentLoaded', function () {
    var calendarCells = document.querySelectorAll('.calendar-body td');
    var selectedCell = null;

    var selectedDate = window.location.href.split('/')[4];

    function clicker(cell) {
        var originalText = cell.textContent;

        if (originalText != "") {
            cell.classList.toggle('clicked');
            selectedCell = cell;
        }
    };
    
    function updateURL(selectedDay) {
        var cellDate = window.location.href;
            cellDate = cellDate.split('-'); 

            selectedDay = selectedCell.textContent.trim();
            var newURL = cellDate[0] + '-' + cellDate[1] + '-' + selectedDay;
        
        window.location.href = newURL;

    } 

    calendarCells.forEach(function (cell) {

        selectedCell = Array.from(calendarCells).find (cell => cell.textContent.trim() === selectedDate.split('-')[2]);
            clicker(selectedCell);

        calendarCells.forEach(function (cell) {
            var originalText = cell.textContent;

            cell.addEventListener('mouseover', function () {
                if (originalText != "") {
//                    this.textContent = "+";
                }
            });

            cell.addEventListener('mouseout', function () {
                this.textContent = originalText;
            });

            cell.addEventListener('click', function () {
                clicker(this);
//                this.textContent = originalText;
                updateURL(this.textContent.trim());

            });
        });
    });
});