// add comment popup
const addComment = document.querySelector(".add-comment");
const closePopup = document.querySelector(".close-popup");
const fade_bg = document.querySelector(".fade-bg");
const commentPopup = document.querySelector(".comment-popup");

addComment.addEventListener("click", function () {
    fade_bg.classList.add("show");
    commentPopup.classList.add("show");
});

// close comment popup
closePopup.addEventListener("click", function () {
    fade_bg.classList.remove("show");
    commentPopup.classList.remove("show");
});

