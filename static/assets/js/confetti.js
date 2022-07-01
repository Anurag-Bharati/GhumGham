const colors = [
    getComputedStyle(document.body).getPropertyValue("--c1"),
    getComputedStyle(document.body).getPropertyValue("--c2")
];


const ghumgham = document.getElementById('ghumgham-nav-ico');
const rect = ghumgham.getBoundingClientRect();
ghumgham.addEventListener('animationstart', (ev) => {
    celebrate()
});

function celebrate() {
    if ($(window).width() > 992) {
        setTimeout(function () {
            confetti({
                particleCount: 5,
                spread: 100,
                ticks: 80,
                startVelocity: 10,
                origin: {y: 0.05, x: 0.06},
                zIndex: 1000000000,
                colors,
                disableForReducedMotion: true,
            });
        }, 280);

    }

}
