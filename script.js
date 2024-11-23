document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contact-form');

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Form submission handling (client-side)
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const name = e.target.elements.name.value;
        const email = e.target.elements.email.value;
        const message = e.target.elements.message.value;

        // Basic form validation
        if (!name || !email || !message) {
            alert('Please fill out all fields');
            return;
        }

        // In a real-world scenario, you would send this to a backend service
        console.log('Form submitted:', { name, email, message });

        // Simulate form submission
        alert('Thank you for your message! I will get back to you soon.');
        contactForm.reset();
    });

    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const fadeInObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Add fade-in animation to sections
    document.querySelectorAll('.about, .projects, .contact').forEach(section => {
        fadeInObserver.observe(section);
    });

    // Publication filters
    const filterButtons = document.querySelectorAll('.filter-btn');
    const publicationCards = document.querySelectorAll('.publication-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            const filter = button.getAttribute('data-filter');

            publicationCards.forEach(card => {
                if (filter === 'all' || card.classList.contains(filter)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Add smooth scroll for all pages
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Mobile navigation toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            navLinks.classList.toggle('show');
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('show');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !navToggle.contains(e.target)) {
                navLinks.classList.remove('show');
            }
        });
    }

    // Set active nav link based on current page
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a').forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Collapsible sections
    const collapsibles = document.querySelectorAll('.collapsible-header');

    collapsibles.forEach(header => {
        // Set initial state
        const content = header.nextElementSibling;
        content.style.display = 'none';

        // Add click event
        header.addEventListener('click', () => {
            console.log('Header clicked'); // Debug log
            header.classList.toggle('active');
            const content = header.nextElementSibling;

            if (content.style.display === 'none') {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        });
    });
});
