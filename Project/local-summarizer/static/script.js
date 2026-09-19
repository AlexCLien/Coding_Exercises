console.log("script.js loaded");

const form = document.getElementById("analysisForm");
const button = document.getElementById("submitButton");
form.addEventListener("submit", function () {
    button.value = "Processing...";
    button.disabled = true;
});