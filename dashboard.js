// =============================================
// WardPulse AI - Dashboard JavaScript
// =============================================
// Dashboard-specific animations and interactions

document.addEventListener('DOMContentLoaded', function() {
    // Animate stat cards on load
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.animation = `fadeInUp 0.5s ease ${index * 0.1}s both`;
    });
});
