// =============================================
// WardPulse AI - Admin JavaScript
// =============================================
// AI summary generation, admin-specific functions

// =============================================
// Generate AI Summary
// =============================================
function generateAISummary() {
    const panel = document.getElementById('aiSummaryPanel');
    const content = document.getElementById('aiSummaryContent');
    if (!panel || !content) return;

    panel.classList.remove('hidden');
    content.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div><p class="text-xs mt-2" style="color: var(--text-muted);">Generating AI insights...</p>';

    // Get CSRF token
    const csrfInput = document.querySelector('[name=csrf_token]');
    const csrfToken = csrfInput ? csrfInput.value : '';

    fetch('/api/ai/summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(r => r.json())
    .then(data => {
        content.textContent = data.summary || 'No summary available.';
        showToast('AI summary generated!', 'success');
    })
    .catch(err => {
        content.textContent = 'Failed to generate AI summary. Please try again.';
        showToast('AI summary failed.', 'error');
    });
}
