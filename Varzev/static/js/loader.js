const loader = document.querySelector(".loader-bg");

window.addEventListener("load", function () {

    setTimeout(function () {
       loader.style.display = 'none';
    }, 3000);
});