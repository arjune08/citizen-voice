// =============================================
// WardPulse AI - Main JavaScript
// =============================================
// Theme toggle, loading screen, scroll animations,
// toast notifications, counter animations, utilities

// =============================================
// Loading Screen
// =============================================
window.addEventListener('load', function() {
    const loader = document.getElementById('loadingScreen');
    if (loader) {
        setTimeout(() => {
            loader.classList.add('hidden');
        }, 50);
    }
});

// =============================================
// Theme Toggle (Dark/Light Mode)
// =============================================
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const newTheme = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('wardpulse-theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Load saved theme
(function() {
    const saved = localStorage.getItem('wardpulse-theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcon(saved);
})();

// =============================================
// Mobile Menu Toggle
// =============================================
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    const icon = document.getElementById('mobileMenuIcon');
    if (menu) {
        menu.classList.toggle('active');
        if (icon) {
            icon.className = menu.classList.contains('active') ? 'fas fa-times text-xl' : 'fas fa-bars text-xl';
        }
    }
}

// =============================================
// Navbar Scroll Effect
// =============================================
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});

// =============================================
// Scroll Animations
// =============================================
function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Stagger the animation delay
                setTimeout(() => {
                    entry.target.classList.add('animated');
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    elements.forEach(el => observer.observe(el));
}

document.addEventListener('DOMContentLoaded', initScrollAnimations);

// =============================================
// Counter Animation
// =============================================
function animateCounters() {
    const counters = document.querySelectorAll('.counter');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target')) || 0;
                const duration = 2000;
                const startTime = performance.now();

                function updateCounter(currentTime) {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    // Ease-out curve
                    const easeOut = 1 - Math.pow(1 - progress, 3);
                    const current = Math.floor(easeOut * target);
                    counter.textContent = current.toLocaleString();

                    if (progress < 1) {
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target.toLocaleString();
                    }
                }

                requestAnimationFrame(updateCounter);
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
}

document.addEventListener('DOMContentLoaded', animateCounters);

// =============================================
// Toast Notifications
// =============================================
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const icons = {
        success: '<i class="fas fa-check-circle text-green-500"></i>',
        error: '<i class="fas fa-times-circle text-red-500"></i>',
        warning: '<i class="fas fa-exclamation-triangle text-yellow-500"></i>',
        info: '<i class="fas fa-info-circle text-blue-500"></i>'
    };

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || icons.info}</span>
        <span class="toast-message">${message}</span>
    `;
    toast.onclick = () => toast.remove();

    container.appendChild(toast);

    // Auto-remove after 4.5 seconds
    setTimeout(() => {
        if (toast.parentNode) toast.remove();
    }, 4500);
}

// =============================================
// Image Preview Utility
// =============================================
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    if (!preview) return;

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.add('active');
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// =============================================
// Password Visibility Toggle
// =============================================
function togglePasswordVisibility(inputId, button) {
    const input = document.getElementById(inputId);
    if (!input) return;

    if (input.type === 'password') {
        input.type = 'text';
        button.innerHTML = '<i class="fas fa-eye-slash"></i>';
    } else {
        input.type = 'password';
        button.innerHTML = '<i class="fas fa-eye"></i>';
    }
}

// =============================================
// GPS Location
// =============================================
function getLocation() {
    if (!navigator.geolocation) {
        showToast('Geolocation is not supported by your browser.', 'error');
        return;
    }

    showToast('Getting your location...', 'info');

    navigator.geolocation.getCurrentPosition(
        function(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            // Set hidden fields
            const latField = document.getElementById('latitude');
            const lngField = document.getElementById('longitude');
            if (latField) latField.value = lat;
            if (lngField) lngField.value = lng;

            // Show status
            const status = document.getElementById('gpsStatus');
            const coords = document.getElementById('gpsCoords');
            if (status) status.classList.remove('hidden');
            if (coords) coords.textContent = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;

            // Show mini map
            const mapDiv = document.getElementById('locationMap');
            if (mapDiv && typeof L !== 'undefined') {
                mapDiv.style.display = 'block';
                const map = L.map('locationMap').setView([lat, lng], 15);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OSM'
                }).addTo(map);
                L.marker([lat, lng]).addTo(map).bindPopup('Your Location').openPopup();
            }

            showToast('Location captured successfully!', 'success');
        },
        function(error) {
            showToast('Could not get location. Please enter address manually.', 'warning');
        },
        { enableHighAccuracy: true, timeout: 10000 }
    );
}

// =============================================
// File Drag & Drop
// =============================================
document.addEventListener('DOMContentLoaded', function() {
    const uploadAreas = document.querySelectorAll('.file-upload');
    uploadAreas.forEach(area => {
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });
        area.addEventListener('dragleave', () => {
            area.classList.remove('dragover');
        });
        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
            const input = area.querySelector('input[type="file"]');
            if (input && e.dataTransfer.files.length > 0) {
                input.files = e.dataTransfer.files;
                input.dispatchEvent(new Event('change'));
            }
        });
    });
});

// =============================================
// Auto-remove flash toasts
// =============================================
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toast').forEach(toast => {
        setTimeout(() => {
            if (toast.parentNode) toast.remove();
        }, 4500);
    });
});
