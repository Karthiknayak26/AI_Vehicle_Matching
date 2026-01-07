// Smart URL selection for deployment
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function fetchVehicles(pickup, drop, userMode = 'fastest') {
    try {
        const response = await fetch(`${API_BASE_URL}/ride/quote`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pickup: { lat: pickup.lat, lon: pickup.lon },
                drop: { lat: drop.lat, lon: drop.lon },
                user_mode: userMode
            })
        })

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`)
        }

        return await response.json()
    } catch (error) {
        console.error('Error fetching vehicles:', error)
        throw error
    }
}

export async function registerVehicle(vehicleData) {
    try {
        const response = await fetch(`${API_BASE_URL}/vehicles/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(vehicleData)
        })

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`)
        }

        return await response.json()
    } catch (error) {
        console.error('Error registering vehicle:', error)
        throw error
    }
}

export async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`)

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`)
        }

        return await response.json()
    } catch (error) {
        console.error('Error checking health:', error)
        throw error
    }
}

// Mock driver data for confirmation screen - Indian drivers from Udupi
export const MOCK_DRIVERS = [
    { name: "Rajesh Kumar", vehicle: "Maruti Swift", plate: "KA 20 AB 1234", rating: 4.9 },
    { name: "Priya Shetty", vehicle: "Hyundai i20", plate: "KA 20 CD 5678", rating: 4.8 },
    { name: "Suresh Nayak", vehicle: "Honda City", plate: "KA 20 EF 9012", rating: 5.0 },
    { name: "Anita Rao", vehicle: "Toyota Innova", plate: "KA 20 GH 3456", rating: 4.7 },
    { name: "Mohan Bhat", vehicle: "Tata Nexon", plate: "KA 20 IJ 7890", rating: 4.9 }
]

export function getRandomDriver() {
    return MOCK_DRIVERS[Math.floor(Math.random() * MOCK_DRIVERS.length)]
}
