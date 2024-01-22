document.addEventListener('DOMContentLoaded', function () {
    var calendarCells = document.querySelectorAll('.calendar-body td');
    var previouslyClickedCell = null;

    calendarCells.forEach(function (cell) {
        
        calendarCells.forEach(function (cell) {
            var originalText = cell.textContent;            
            cell.addEventListener('mouseover', function () {
                if (originalText != "") {
                    this.textContent = "A12"
                }
               
            });

            cell.addEventListener('mouseout', function () {
                this.textContent = originalText;
            });

            cell.addEventListener('click', function () {
            var originalText = cell.textContent;
                if (originalText != "") {
                    this.classList.toggle('clicked');
        
                    if (previouslyClickedCell && previouslyClickedCell !== this) {
                        previouslyClickedCell.classList.remove('clicked');
                    }
        
                    previouslyClickedCell = this;
                }
            });
        });
    });
})