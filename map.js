// =============================================
// WardPulse AI - Map JavaScript
// =============================================
// Leaflet map initialization and marker utilities

// Map is initialized inline in templates that need it
// This file provides shared map utilities

// =============================================
// Priority Color Map
// =============================================
const PRIORITY_COLORS = {
    critical: '#dc2626',
    high: '#f97316',
    medium: '#f59e0b',
    low: '#10b981'
};

// =============================================
// Create Priority Marker
// =============================================
function createPriorityMarker(lat, lng, priority) {
    const color = PRIORITY_COLORS[priority] || '#6366f1';
    return L.circleMarker([lat, lng], {
        radius: 10,
        fillColor: color,
        color: '#ffffff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.8
    });
}
