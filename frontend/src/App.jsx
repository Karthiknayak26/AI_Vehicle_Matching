import { useState } from 'react'
import MapContainer from './components/MapContainer'
import RidePlanningCard from './components/RidePlanningCard'
import AIProcessingOverlay from './components/AIProcessingOverlay'
import VehicleResultsPanel from './components/VehicleResultsPanel'
import ConfirmationScreen from './components/ConfirmationScreen'
import WelcomePage from './components/WelcomePage'
import ThemeToggle from './components/ThemeToggle'
import { geocode } from './utils/geocoding'
import { fetchVehicles, getRandomDriver } from './utils/api'
import './styles/App.css'

const AppStates = {
    WELCOME: 'welcome',
    IDLE: 'idle',
    SEARCHING: 'searching',
    RESULTS: 'results',
    SELECTED: 'selected',
    CONFIRMED: 'confirmed'
}

function App() {
    const [state, setState] = useState(AppStates.WELCOME)
    const [theme, setTheme] = useState('dark')
    const [pickup, setPickup] = useState(null)
    const [drop, setDrop] = useState(null)
    const [preference, setPreference] = useState('fastest')
    const [vehicles, setVehicles] = useState([])
    const [selectedVehicle, setSelectedVehicle] = useState(null)
    const [driver, setDriver] = useState(null)
    const [quoteData, setQuoteData] = useState(null)
    const [animatingVehicle, setAnimatingVehicle] = useState(null)

    const handleSearch = async (pickupName, dropName, userPreference) => {
        // Geocode locations
        const pickupCoords = geocode(pickupName)
        const dropCoords = geocode(dropName)

        setPickup(pickupCoords)
        setDrop(dropCoords)
        setPreference(userPreference)
        setState(AppStates.SEARCHING)

        try {
            // Simulate AI processing delay
            await new Promise(resolve => setTimeout(resolve, 3000))

            // Fetch vehicles from API
            const data = await fetchVehicles(pickupCoords, dropCoords, userPreference)
            setVehicles(data.available_vehicles)
            setQuoteData(data)
            setState(AppStates.RESULTS)
        } catch (error) {
            console.error('Error fetching vehicles:', error)
            // Fallback to idle state on error
            setState(AppStates.IDLE)
            alert(error.message || 'Error fetching vehicles. Please make sure the API server is running.')
        }
    }

    const handleSelectVehicle = (vehicle) => {
        setSelectedVehicle(vehicle)
        setState(AppStates.SELECTED)
    }

    const handleConfirm = () => {
        setDriver(getRandomDriver())
        setState(AppStates.CONFIRMED)

        // Start vehicle animation (5 seconds for demo, use real ETA for production)
        if (selectedVehicle && pickup) {
            // Mock starting position (slightly offset from pickup)
            const startLat = pickup.lat + 0.01
            const startLon = pickup.lon - 0.01

            setAnimatingVehicle({
                vehicleId: selectedVehicle.vehicle_id,
                startLat: startLat,
                startLon: startLon,
                endLat: pickup.lat,
                endLon: pickup.lon,
                startTime: Date.now(),
                duration: 5000 // 5 seconds for demo (use selectedVehicle.eta_pickup * 60 * 1000 for real-time)
            })
        }
    }

    const handleReset = () => {
        setState(AppStates.IDLE)
        setPickup(null)
        setDrop(null)
        setVehicles([])
        setSelectedVehicle(null)
        setDriver(null)
        setQuoteData(null)
        setAnimatingVehicle(null)
    }

    const handleGetStarted = () => {
        setState(AppStates.IDLE)
    }

    const toggleTheme = () => {
        const newTheme = theme === 'dark' ? 'light' : 'dark'
        setTheme(newTheme)
        document.documentElement.setAttribute('data-theme', newTheme)
    }

    return (
        <div className="app">
            {state !== AppStates.WELCOME && (
                <ThemeToggle theme={theme} onToggle={toggleTheme} />
            )}

            {state === AppStates.WELCOME && (
                <WelcomePage onGetStarted={handleGetStarted} />
            )}

            <MapContainer
                pickup={pickup}
                drop={drop}
                showRoute={state === AppStates.RESULTS || state === AppStates.SELECTED || state === AppStates.CONFIRMED}
                vehicles={state === AppStates.RESULTS || state === AppStates.SELECTED || state === AppStates.CONFIRMED ? vehicles : null}
                animatingVehicle={animatingVehicle}
                selectedVehicle={selectedVehicle}
                theme={theme}
            />

            {state === AppStates.IDLE && (
                <RidePlanningCard onSearch={handleSearch} />
            )}

            {state === AppStates.SEARCHING && (
                <AIProcessingOverlay />
            )}

            {state === AppStates.RESULTS && (
                <VehicleResultsPanel
                    vehicles={vehicles}
                    quoteData={quoteData}
                    onSelect={handleSelectVehicle}
                    onBack={handleReset}
                />
            )}

            {state === AppStates.SELECTED && (
                <VehicleResultsPanel
                    vehicles={vehicles}
                    quoteData={quoteData}
                    selectedVehicle={selectedVehicle}
                    onConfirm={handleConfirm}
                    onBack={() => setState(AppStates.RESULTS)}
                />
            )}

            {state === AppStates.CONFIRMED && (
                <ConfirmationScreen
                    vehicle={selectedVehicle}
                    driver={driver}
                    quoteData={quoteData}
                    onReset={handleReset}
                />
            )}
        </div>
    )
}

export default App
