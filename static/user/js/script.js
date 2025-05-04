// JavaScript for QuickTrade

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Email validation function
    window.isValidEmail = function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    // Form validation for registration
    const registrationForm = document.getElementById('registration-form');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(event) {
            const emailInput = document.getElementById('email');
            if (emailInput && !isValidEmail(emailInput.value)) {
                event.preventDefault();
                alert('Please enter a valid email address.');
            }
        });
    }

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Price range slider for product search
    const priceRangeMin = document.getElementById('price_min');
    const priceRangeMax = document.getElementById('price_max');
    if (priceRangeMin && priceRangeMax) {
        // Display the values as the user adjusts the sliders
        priceRangeMin.addEventListener('input', function() {
            document.getElementById('price_min_display').textContent = '$' + this.value;
        });
        
        priceRangeMax.addEventListener('input', function() {
            document.getElementById('price_max_display').textContent = '$' + this.value;
        });
    }
});