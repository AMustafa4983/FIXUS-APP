document.addEventListener("DOMContentLoaded", function() {
    var toggleButtons = document.querySelectorAll('.toggle-btn input');

    toggleButtons.forEach(function(button) {
        button.addEventListener('change', function() {
            document.getElementById('selected_xray_type').value = this.value;
        });
    });
});

function showLoadingScreen() {
    var overlay = document.getElementById("overlay");
    overlay.style.display = "flex";
}