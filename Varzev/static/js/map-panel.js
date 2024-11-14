const closeMap = document.querySelector(".close-map");
const fadeBg = document.querySelector(".fade-bg");
const mapField = document.querySelector(".map-wrapper");
const mapBtn = document.querySelector(".submit-address");

mapBtn.addEventListener("click", function () {
    fadeBg.classList.add("show");
    mapField.classList.add("show");
});

closeMap.addEventListener("click", function () {
    fadeBg.classList.remove("show");
    mapField.classList.remove("show");
});