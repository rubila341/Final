// Файл: static/scripts/parallax.js

document.addEventListener('scroll', function() {
    const parallax = document.querySelector('.parallax');
    const scrolled = window.scrollY;
    parallax.style.backgroundPositionY = `${scrolled * 0.5}px`;
});
