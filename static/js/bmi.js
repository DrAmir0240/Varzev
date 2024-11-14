const bmiBtn = document.querySelector(".bmi-btn");
const userBmi = document.querySelector(".user-bmi");
const checkHealth = document.querySelector(".check-health");
const bmiPanel = document.querySelector(".bmi-show");
const bmiForm = document.querySelector(".request-detail");
const weightError = document.querySelector(".bmi-error__weight");
const heightError = document.querySelector(".bmi-error__height");

let status = '';

bmiBtn.addEventListener("click", function () {
    let height = document.querySelector(".height-input").value;
    let weight = document.querySelector(".weight-input").value;

    let bmi = (weight / (Math.pow(height, 2)) * 10000).toFixed(1);

    userBmi.textContent = bmi;

    if (bmi < 18.5) {
        checkHealth.innerHTML = 'کمبود وزن';
    } else if (bmi > 18.5 && bmi < 24.9) {
        checkHealth.innerHTML = 'وزن سلامت';
    } else if (bmi > 25 && bmi < 29.9) {
        checkHealth.innerHTML = 'اضافه وزن';
    } else if (bmi > 30) {
        checkHealth.innerHTML = 'چاق';
    }

    if (height === '') {
        heightError.classList.add("show");
    } else {
        heightError.classList.remove("show");
    }

    if (weight === '') {
        weightError.classList.add("show");
    } else {
        weightError.classList.remove("show");
    }

    if (height && weight !== '') {
        bmiPanel.classList.add("show");
        bmiForm.style.display = 'none';
    }

})