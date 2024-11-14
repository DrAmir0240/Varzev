// Click on brand input and show tick
const brandInput = document.querySelectorAll(".square-input");

brandInput.forEach((input) => {
    input.addEventListener("click", function () {
        input.classList.toggle("show");
    });
});

// toggle switch btn
const switchBtn = document.querySelectorAll(".switch-btn");
switchBtn.forEach((btn) => {
    btn.addEventListener("click", function () {
        btn.classList.toggle("active");
    });
});

// Click on sort by and show filter option
const sortFilterBy = document.querySelector(".sort-by__filter");
const filterMobileWrapper = document.querySelector(".filter-mobile__wrapper");

sortFilterBy.addEventListener("click", function () {
    filterMobileWrapper.classList.toggle("active");
});

// select filter option
const filterOption = document.querySelectorAll(".filter-option .filter-option__item");
filterOption.forEach((option) => {
    option.addEventListener("click", function () {
        filterOption.forEach((item) => {
            item.classList.remove("active");
        });
        option.classList.add("active");
    });
});

// click on filter option and replace text
const filterOptions = document.querySelectorAll(".filter-mobile__wrapper .filter-option__item");
filterOptions.forEach((option) => {
    option.addEventListener("click", function () {
        sortFilterBy.textContent = option.textContent;
    });
});