// QuickTrade frontend interactions. Marketplace data and navigation remain Django-powered.
document.addEventListener('DOMContentLoaded', function () {
    // Bootstrap enhancements are optional on pages that do not use them.
    if (window.bootstrap) {
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (element) {
            bootstrap.Tooltip.getOrCreateInstance(element);
        });
        document.querySelectorAll('[data-bs-toggle="popover"]').forEach(function (element) {
            bootstrap.Popover.getOrCreateInstance(element);
        });
    }

    // Responsive navigation for the custom QuickTrade header.
    var menuToggle = document.querySelector('.qt-menu-toggle');
    var navigation = document.querySelector('.qt-navigation');
    if (menuToggle && navigation) {
        menuToggle.addEventListener('click', function () {
            var isOpen = navigation.classList.toggle('is-open');
            menuToggle.setAttribute('aria-expanded', String(isOpen));
            var icon = menuToggle.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars', !isOpen);
                icon.classList.toggle('fa-times', isOpen);
            }
        });
        navigation.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navigation.classList.remove('is-open');
                menuToggle.setAttribute('aria-expanded', 'false');
                var icon = menuToggle.querySelector('i');
                if (icon) {
                    icon.classList.add('fa-bars');
                    icon.classList.remove('fa-times');
                }
            });
        });
        window.addEventListener('resize', function () {
            if (window.innerWidth > 960) {
                navigation.classList.remove('is-open');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Horizontal product rail arrows scroll real Django-rendered listings.
    document.querySelectorAll('[data-scroll-direction]').forEach(function (button) {
        button.addEventListener('click', function () {
            var rail = button.closest('.qt-listings-track-wrap');
            rail = rail ? rail.querySelector('[data-listings-rail]') : null;
            if (!rail) return;
            var direction = Number(button.getAttribute('data-scroll-direction')) || 1;
            rail.scrollBy({ left: direction * Math.max(rail.clientWidth * 0.8, 240), behavior: 'smooth' });
        });
    });

    // Keep the existing registration email validation helper available.
    window.isValidEmail = function (email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    };
    var registrationForm = document.getElementById('registration-form');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function (event) {
            var emailInput = document.getElementById('email');
            if (emailInput && !window.isValidEmail(emailInput.value)) {
                event.preventDefault();
                alert('Please enter a valid email address.');
                emailInput.focus();
            }
        });
    }

    // Dismiss Django/Bootstrap alerts after a short delay without breaking pages
    // that do not load Bootstrap's JavaScript.
    window.setTimeout(function () {
        document.querySelectorAll('.alert').forEach(function (alertElement) {
            if (window.bootstrap && bootstrap.Alert) {
                bootstrap.Alert.getOrCreateInstance(alertElement).close();
            }
        });
    }, 6000);

    // Product filters use rupees, matching QuickTrade's INR pricing.
    var priceRangeMin = document.getElementById('price_min');
    var priceRangeMax = document.getElementById('price_max');
    var minDisplay = document.getElementById('price_min_display');
    var maxDisplay = document.getElementById('price_max_display');
    if (priceRangeMin && minDisplay) {
        var updateMin = function () { minDisplay.textContent = '₹' + priceRangeMin.value; };
        priceRangeMin.addEventListener('input', updateMin);
        updateMin();
    }
    if (priceRangeMax && maxDisplay) {
        var updateMax = function () { maxDisplay.textContent = '₹' + priceRangeMax.value; };
        priceRangeMax.addEventListener('input', updateMax);
        updateMax();
    }
});