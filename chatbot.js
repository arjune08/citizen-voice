// =============================================
// WardPulse AI - Chatbot JavaScript
// =============================================
// AI chatbot widget toggle and message handling

// =============================================
// Toggle Chatbot Window
// =============================================
function toggleChatbot() {
    const window = document.getElementById('chatbotWindow');
    if (window) {
        window.classList.toggle('active');
        // Focus input when opening
        if (window.classList.contains('active')) {
            const input = document.getElementById('chatInput');
            if (input) input.focus();
        }
    }
}

// =============================================
// Send Chat Message
// =============================================
function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const messages = document.getElementById('chatMessages');
    if (!input || !messages) return;

    const message = input.value.trim();
    if (!message) return;

    // Add user message
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-message user';
    userMsg.textContent = message;
    messages.appendChild(userMsg);

    // Clear input
    input.value = '';

    // Scroll to bottom
    messages.scrollTop = messages.scrollHeight;

    // Add typing indicator
    const typing = document.createElement('div');
    typing.className = 'typing-indicator';
    typing.innerHTML = '<span></span><span></span><span></span>';
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;

    // Get CSRF token
    const csrfInput = document.querySelector('[name=csrf_token]');
    const csrfToken = csrfInput ? csrfInput.value : '';

    // Send to API
    fetch('/api/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ message: message })
    })
    .then(r => r.json())
    .then(data => {
        // Remove typing indicator
        typing.remove();

        // Add bot response
        const botMsg = document.createElement('div');
        botMsg.className = 'chat-message bot';
        botMsg.innerHTML = formatChatResponse(data.response || 'Sorry, I could not process your request.');
        messages.appendChild(botMsg);
        messages.scrollTop = messages.scrollHeight;
    })
    .catch(err => {
        typing.remove();
        const errorMsg = document.createElement('div');
        errorMsg.className = 'chat-message bot';
        errorMsg.textContent = 'Sorry, something went wrong. Please try again.';
        messages.appendChild(errorMsg);
        messages.scrollTop = messages.scrollHeight;
    });
}

// =============================================
// Format Chat Response
// =============================================
function formatChatResponse(text) {
    // Convert markdown-like formatting to HTML
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>')
        .replace(/•/g, '<br>•');
}

// =============================================
// Keyboard shortcut: Escape to close chatbot
// =============================================
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const chatWindow = document.getElementById('chatbotWindow');
        if (chatWindow && chatWindow.classList.contains('active')) {
            toggleChatbot();
        }
    }
});
