// mobile menu
const menuIcon = document.querySelector(".hamburger-icon");
const closeMenu = document.querySelector(".close-menu");
const mobileMenu = document.querySelector(".mobile-menu");

menuIcon.addEventListener("click", function () {
    mobileMenu.classList.add("show");
});

closeMenu.addEventListener("click", function () {
    mobileMenu.classList.remove("show");
});

const header = document.querySelector(".header-section");

window.onscroll=()=> {
    if (window.scrollY >= 70 ) {
        header.classList.add("change");
    } else {
        header.classList.remove("change");
    }
}

const accordionIcon = document.querySelectorAll(".accordion-icon");
const accordionTarget = document.querySelectorAll(".accordion-target");

accordionIcon.forEach((icon,i) => {
    icon.addEventListener("click", function () {
        accordionTarget.forEach(accordion => {
            accordion.classList.remove("active");
        });
        accordionTarget[i].classList.add("active");
    });
});

// delete photo on user-info page
const deleteImg = document.querySelectorAll(".delete-img");
const relatedPhoto = document.querySelectorAll(".related-photo");

deleteImg.forEach((del,i)=> {
    del.addEventListener("click", function () {
        relatedPhoto[i].style.display = 'none';
    });
});

// sortBy for swiper on index page
const sortBy = document.querySelectorAll(".sort-by_swiper");
const swiperTitle = document.querySelectorAll(".team-swiper");
sortBy.forEach(item => {
    item.addEventListener("click", function () {
        sortBy.forEach(sort => {
            sort.classList.remove("active");
        })
        let dataType = item.getAttribute("data-name");

        swiperTitle.forEach(swiper => {
            if (swiper.getAttribute("data-name") === dataType) {
                swiper.classList.add("active");
            } else {
                swiper.classList.remove("active");
            }
        })
        item.classList.add("active");
    });
});

// sortBy for place-swiper on index page
const sortPlace = document.querySelectorAll(".sort-by_place");
const swiperPlace = document.querySelectorAll(".place-swiper");
sortPlace.forEach(item => {
    item.addEventListener("click", function () {
        sortPlace.forEach(sort => {
            sort.classList.remove("active");
        })
        let dataType = item.getAttribute("data-name");

        swiperPlace.forEach(swiper => {
            if (swiper.getAttribute("data-name") === dataType) {
                swiper.classList.add("active");
            } else {
                swiper.classList.remove("active");
            }
        })
        item.classList.add("active");
    });
});