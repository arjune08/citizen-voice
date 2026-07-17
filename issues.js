// =============================================
// WardPulse AI - Issues JavaScript
// =============================================
// Voting functionality, AJAX interactions

// =============================================
// Vote on Issue (AJAX)
// =============================================
function voteIssue(issueId, button) {
    // Get CSRF token from the page
    const csrfMeta = document.querySelector('[name=csrf_token]');
    const csrfToken = csrfMeta ? csrfMeta.value : '';

    fetch(`/api/vote/${issueId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (response.status === 401) {
            showToast('Please log in to vote.', 'warning');
            window.location.href = '/login';
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return;

        if (data.error) {
            showToast(data.error, 'error');
            return;
        }

        // Update vote count on the button
        const countSpan = button.querySelector('.vote-count');
        if (countSpan) {
            countSpan.textContent = data.votes_count;
        }

        // Toggle voted state
        if (data.voted) {
            button.classList.add('voted');
            showToast('Vote added! 👍', 'success');
        } else {
            button.classList.remove('voted');
            showToast('Vote removed.', 'info');
        }

        // Update detail page elements if they exist
        const sideCount = document.getElementById('voteSideCount');
        const mainCount = document.getElementById('voteCountDisplay');
        if (sideCount) sideCount.textContent = data.votes_count;
        if (mainCount) mainCount.textContent = data.votes_count;

        // Update detail page button text
        const detailBtn = document.getElementById('voteDetailBtn');
        if (detailBtn) {
            const span = detailBtn.querySelector('span');
            if (span) span.textContent = data.voted ? 'Voted' : 'Upvote';
            if (data.voted) {
                detailBtn.classList.remove('btn-primary');
                detailBtn.classList.add('btn-outline');
            } else {
                detailBtn.classList.remove('btn-outline');
                detailBtn.classList.add('btn-primary');
            }
        }
    })
    .catch(err => {
        console.error('Vote error:', err);
        showToast('Failed to vote. Please try again.', 'error');
    });
}
