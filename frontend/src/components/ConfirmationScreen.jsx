import { useState, useEffect } from 'react'
import './ConfirmationScreen.css'

function ConfirmationScreen({ vehicle, driver, quoteData, onReset }) {
    const [eta, setEta] = useState(vehicle.eta_pickup)

    useEffect(() => {
        // Simulate countdown
        const interval = setInterval(() => {
            setEta(prev => Math.max(0, prev - 0.1))
        }, 6000) // Update every 6 seconds

        return () => clearInterval(interval)
    }, [])

    return (
        <div className="confirmation-screen glass fade-in">
            <div className="confirmation-header">
                <div className="success-icon">✅</div>
                <h2>Ride Confirmed!</h2>
                <p>Your driver is on the way</p>
            </div>

            <div className="driver-card">
                <div className="driver-avatar">
                    {driver.name.charAt(0)}
                </div>
                <div className="driver-info">
                    <h3>{driver.name}</h3>
                    <div className="driver-rating">
                        ⭐ {driver.rating} • {vehicle.vehicle_type}
                    </div>
                    <div className="driver-vehicle">
                        {driver.vehicle} • {driver.plate}
                    </div>
                </div>
            </div>

            <div className="eta-card">
                <div className="eta-icon pulse">📍</div>
                <div className="eta-info">
                    <div className="eta-label">Arriving in</div>
                    <div className="eta-time">{Math.ceil(eta)} minutes</div>
                </div>
            </div>

            <div className="trip-details">
                <h3>Trip Details</h3>
                <div className="detail-row">
                    <span className="detail-icon">📍</span>
                    <span className="detail-label">Distance</span>
                    <span className="detail-value">{quoteData.distance} km</span>
                </div>
                <div className="detail-row">
                    <span className="detail-icon">⏱️</span>
                    <span className="detail-label">Duration</span>
                    <span className="detail-value">{quoteData.estimated_duration} min</span>
                </div>
                <div className="detail-row">
                    <span className="detail-icon">🚦</span>
                    <span className="detail-label">Traffic</span>
                    <span className="detail-value">{quoteData.surge_reason}</span>
                </div>
            </div>

            <div className="fare-summary">
                <h3>Fare Summary</h3>
                <div className="fare-row">
                    <span>Base fare</span>
                    <span>${vehicle.fare_breakdown.base_fare.toFixed(2)}</span>
                </div>
                <div className="fare-row">
                    <span>Distance</span>
                    <span>${vehicle.fare_breakdown.distance_cost.toFixed(2)}</span>
                </div>
                <div className="fare-row">
                    <span>Time</span>
                    <span>${vehicle.fare_breakdown.time_cost.toFixed(2)}</span>
                </div>
                <div className="fare-row">
                    <span>Surge ({vehicle.fare_breakdown.surge_multiplier}x)</span>
                    <span>$0.00</span>
                </div>
                <div className="fare-total">
                    <span>Total</span>
                    <span>${vehicle.final_fare.toFixed(2)}</span>
                </div>
            </div>

            <div className="action-buttons">
                <button className="track-button">
                    📍 Track Driver
                </button>
                <button className="new-ride-button" onClick={onReset}>
                    🚗 New Ride
                </button>
            </div>

            <div className="demo-notice">
                <small>🎭 This is a demo. Driver tracking and payment are simulated.</small>
            </div>
        </div>
    )
}

export default ConfirmationScreen
