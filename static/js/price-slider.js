// Price Input Slider
const slider1 = document.getElementById('slider-1');
const slider2 = document.getElementById('slider-2');
const range1 = document.getElementById('range-1');
const range2 = document.getElementById('range-2');
const slider_track = document.querySelector(".slider_track");
const maxValue = document.getElementById('slider-1').max;
let space = 0;

window.onload=()=> {
    inputOne();
    inputTwo();
}
// set input Slider One
function inputOne() {
    if (slider2.value - slider1.value <= space) {
        slider1.value = slider2.value - space;
    }
    range1.textContent = slider1.value;
    bgFill();
}
// set input Slider Two
function inputTwo() {
    if (slider2.value - slider1.value <= space) {
        slider2.value = slider1.value - space;
    }
    range2.textContent = slider2.value;
    bgFill();
}
// make background for input Slider
function bgFill() {
    let percent1 = (slider1.value / maxValue) * 100;
    let percent2 = (slider2.value / maxValue) * 100;
    slider_track.style.background = `linear-gradient(to left, #f4f4f4 ${percent1}%, #19d686 ${percent1}%
    , #19d686 ${percent2}%, #f4f4f4 ${percent2}%)`;
}