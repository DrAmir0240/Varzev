var swiper = new Swiper(".mySwiper", {
    autoplay: true,
    spaceBetween: 30,
    speed: 500,
    breakpoints: {
        992: {
            slidesPerView: 3
        },
        768: {
            slidesPerView: 2
        },
        0: {
            slidesPerView: 1
        }
    },
});

var swiper2 = new Swiper(".suggest-swiper", {
    autoplay: true,
    spaceBetween: 20,
    speed: 500,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        1198: {
            slidesPerView: 4
        },
        992: {
            slidesPerView: 3
        },
        768: {
            slidesPerView: 3
        },
        468: {
            slidesPerView: 2
        },
        0: {
            slidesPerView: 1
        }
    },
});

var swiper3 = new Swiper(".place-swiper", {
    autoplay: true,
    spaceBetween: 20,
    speed: 500,
    breakpoints: {
        1198: {
            slidesPerView: 5
        },
        992: {
            slidesPerView: 4
        },
        768: {
            slidesPerView: 3
        },
        468: {
            slidesPerView: 2
        },
        0: {
            slidesPerView: 1
        }
    },
});

var swiper4 = new Swiper(".team-swiper", {
    autoplay: true,
    spaceBetween: 20,
    speed: 500,
    breakpoints: {
        1198: {
            slidesPerView: 5
        },
        992: {
            slidesPerView: 4
        },
        768: {
            slidesPerView: 3
        },
        468: {
            slidesPerView: 2
        },
        0: {
            slidesPerView: 1
        }
    },
});

var swiper5 = new Swiper(".selection-swiper", {
    autoplay: true,
    spaceBetween: 30,
    speed: 500,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        992: {
            slidesPerView: 3
        },
        768: {
            slidesPerView: 2
        },
        0: {
            slidesPerView: 1
        }
    },
});

var swiper6 = new Swiper(".slider-swiper", {
    autoplay: true,
    spaceBetween: 0,
    slidesPerView: 1,
    speed: 500,
    pagination: {
        el: ".swiper-pagination",
    },
});

var swiper7 = new Swiper(".mySwiper", {
    autoplay: true,
    loop: true,
    slidesPerView: 4,
    spaceBetween: 20,
    speed: 500,
    watchSlidesVisibility: true,
});

var swiper8 = new Swiper(".product_single", {
    spaceBetween: 20,
    thumbs: {
        swiper: swiper7,
    },
});

var swiper9 = new Swiper(".slider-swiper2", {
    autoplay: true,
    spaceBetween: 0,
    slidesPerView: 1,
    speed: 500,
    pagination: {
        el: ".swiper-pagination",
    },
});