// =============================================
// WardPulse AI - Auth JavaScript
// =============================================
// Password strength meter, form validation,
// confirm password matching

// =============================================
// Password Strength Checker
// =============================================
function checkPasswordStrength(password) {
    const bar = document.getElementById('passwordStrengthBar');
    const text = document.getElementById('passwordStrengthText');
    if (!bar || !text) return;

    let strength = 0;
    let label = '';

    // Length check
    if (password.length >= 6) strength++;
    if (password.length >= 8) strength++;

    // Character variety
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;

    // Remove old classes
    bar.className = 'password-strength-bar';

    if (password.length === 0) {
        label = 'Enter a password';
    } else if (strength <= 1) {
        bar.classList.add('strength-weak');
        label = '🔴 Weak';
    } else if (strength <= 2) {
        bar.classList.add('strength-fair');
        label = '🟡 Fair';
    } else if (strength <= 3) {
        bar.classList.add('strength-good');
        label = '🟢 Good';
    } else {
        bar.classList.add('strength-strong');
        label = '💪 Strong';
    }

    text.textContent = label;
}

// =============================================
// Confirm Password Matching
// =============================================
document.addEventListener('DOMContentLoaded', function() {
    const confirmField = document.getElementById('confirmPassword');
    const passwordField = document.getElementById('regPassword');
    const matchText = document.getElementById('passwordMatch');

    if (confirmField && passwordField && matchText) {
        confirmField.addEventListener('input', function() {
            if (this.value && this.value !== passwordField.value) {
                matchText.classList.remove('hidden');
            } else {
                matchText.classList.add('hidden');
            }
        });
    }
});
