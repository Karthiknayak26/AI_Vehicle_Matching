// Simulate traffic route with color-coded segments
export function createTrafficRoute(pickup, drop, segments = 5) {
    const route = []

    for (let i = 0; i <= segments; i++) {
        const t = i / segments
        const lat = pickup.lat + (drop.lat - pickup.lat) * t
        const lon = pickup.lon + (drop.lon - pickup.lon) * t
        route.push([lat, lon])
    }

    return route
}

export function simulateTraffic(routePoints) {
    // Simulate traffic intensity for each segment
    return routePoints.slice(0, -1).map((_, i) => {
        const intensity = Math.random()

        if (intensity < 0.4) return 'green'   // 40% chance - Low traffic
        if (intensity < 0.75) return 'yellow'  // 35% chance - Medium traffic
        return 'red'                           // 25% chance - High traffic
    })
}

export function getTrafficColor(intensity) {
    const colors = {
        green: '#10b981',   // Low traffic
        yellow: '#f59e0b',  // Medium traffic
        red: '#ef4444'      // High traffic
    }
    return colors[intensity] || colors.green
}

export function getTrafficLabel(intensity) {
    const labels = {
        green: 'Light Traffic',
        yellow: 'Moderate Traffic',
        red: 'Heavy Traffic'
    }
    return labels[intensity] || 'Unknown'
}
