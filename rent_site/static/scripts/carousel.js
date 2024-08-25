const carouselContainer = document.querySelector('.carousel-container');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');

let index = 0;

function showNext() {
    index++;
    if (index >= document.querySelectorAll('.carousel-item').length) {
        index = 0;
    }
    updateCarousel();
}

function showPrev() {
    index--;
    if (index < 0) {
        index = document.querySelectorAll('.carousel-item').length - 1;
    }
    updateCarousel();
}

function updateCarousel() {
    const width = document.querySelector('.carousel-item').clientWidth;
    carouselContainer.style.transform = `translateX(${-width * index}px)`;
}

nextBtn.addEventListener('click', showNext);
prevBtn.addEventListener('click', showPrev);
