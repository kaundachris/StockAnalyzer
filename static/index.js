document.addEventListener("DOMContentLoaded", function() {
    const year = document.getElementById("copyright")
    date = new Date()
    year.textContent = date.getFullYear()
})
