document.addEventListener('DOMContentLoaded', () => {
    // Scroll Reveal Intersection Observer
    const reveals = document.querySelectorAll('.reveal');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                // Add a small delay based on index for staggered effect
                setTimeout(() => {
                    entry.target.classList.add('active');
                }, i * 100 % 500); // Caps delay but keeps stagger
                revealObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    reveals.forEach(el => revealObserver.observe(el));

    // Navbar Scroll Effect
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        const isLight = document.body.classList.contains('light-mode');
        if (window.scrollY > 50) {
            navbar.style.background = isLight ? '#ffffff' : 'rgba(7, 13, 25, 0.98)';
            navbar.style.boxShadow = isLight
                ? '0 2px 20px rgba(139, 92, 246, 0.12)'
                : '0 2px 20px rgba(0,0,0,0.4)';
            navbar.style.padding = '5px 5%';
            navbar.style.height = '70px';
        } else {
            navbar.style.background = isLight ? '#ffffff' : 'rgba(7, 13, 25, 0.85)';
            navbar.style.boxShadow = isLight
                ? '0 2px 16px rgba(139, 92, 246, 0.1)'
                : 'none';
            navbar.style.padding = '0 5%';
            navbar.style.height = '80px';
        }
    });
});
