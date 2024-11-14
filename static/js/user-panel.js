//Show user Panel
const userBtn = document.querySelector(".user-panel");
const userPanel = document.querySelector(".header-user__panel");
userBtn.addEventListener("click", function () {
    userPanel.classList.toggle("show");
});