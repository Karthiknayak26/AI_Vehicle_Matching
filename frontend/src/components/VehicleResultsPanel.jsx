import './VehicleResultsPanel.css'

const VEHICLE_ICONS = {
    economy: '🚗',
    sedan: '🚙',
    suv: '🚐'
}

function VehicleResultsPanel({ vehicles, quoteData, selectedVehicle, onSelect, onConfirm, onBack }) {
    const getScoreStars = (score) => {
        const stars = Math.round(score * 5)
        return '⭐'.repeat(stars) + '☆'.repeat(5 - stars)
    }

    const getReason = (vehicle, index) => {
        if (index === 0) {
            if (quoteData?.user_mode === 'fastest') return 'Best for speed'
            if (quoteData?.user_mode === 'cheapest') return 'Best price'
            return 'Best overall'
        }
        return 'Alternative option'
    }

    return (
        <div className="results-panel glass fade-in">
            <div className="panel-header">
                <button className="back-button" onClick={onBack}>
                    ← Back
                </button>
                <div>
                    <h2>Available Vehicles</h2>
                    <p>{quoteData?.distance} km • {quoteData?.estimated_duration} min</p>
                </div>
            </div>

            <div className="vehicles-list">
                {vehicles.map((vehicle, index) => (
                    <div
                        key={vehicle.vehicle_id}
                        className={`vehicle-card ${index === 0 ? 'recommended' : ''} ${selectedVehicle?.vehicle_id === vehicle.vehicle_id ? 'selected' : ''}`}
                        onClick={() => !selectedVehicle && onSelect(vehicle)}
                    >
                        <div className="vehicle-header">
                            <div className="vehicle-icon">
                                {VEHICLE_ICONS[vehicle.vehicle_type] || '🚗'}
                            </div>
                            <div className="vehicle-info">
                                <h3>{vehicle.vehicle_type.toUpperCase()}</h3>
                                <div className="vehicle-id">{vehicle.vehicle_id}</div>
                            </div>
                            <div className="vehicle-score">
                                {getScoreStars(vehicle.score)}
                            </div>
                        </div>

                        <div className="vehicle-stats">
                            <div className="stat">
                                <span className="stat-icon">📍</span>
                                <span className="stat-value">{vehicle.eta_pickup} min away</span>
                            </div>
                            <div className="stat">
                                <span className="stat-icon">⏱️</span>
                                <span className="stat-value">{vehicle.eta_trip} min trip</span>
                            </div>
                            <div className="stat">
                                <span className="stat-icon">💰</span>
                                <span className="stat-value">${vehicle.final_fare.toFixed(2)}</span>
                            </div>
                        </div>

                        {index === 0 && (
                            <div className="recommendation-badge">
                                ✨ {getReason(vehicle, index)}
                            </div>
                        )}

                        {!selectedVehicle && (
                            <button className="select-button">
                                Select Vehicle
                            </button>
                        )}
                    </div>
                ))}
            </div>

            {selectedVehicle && (
                <div className="confirm-section">
                    <div className="fare-details">
                        <h3>Fare Breakdown</h3>
                        <div className="fare-item">
                            <span>Base fare</span>
                            <span>${selectedVehicle.fare_breakdown.base_fare.toFixed(2)}</span>
                        </div>
                        <div className="fare-item">
                            <span>Distance ({quoteData?.distance} km)</span>
                            <span>${selectedVehicle.fare_breakdown.distance_cost.toFixed(2)}</span>
                        </div>
                        <div className="fare-item">
                            <span>Time ({quoteData?.estimated_duration} min)</span>
                            <span>${selectedVehicle.fare_breakdown.time_cost.toFixed(2)}</span>
                        </div>
                        <div className="fare-item">
                            <span>Surge ({selectedVehicle.fare_breakdown.surge_multiplier}x)</span>
                            <span>$0.00</span>
                        </div>
                        <div className="fare-total">
                            <span>Total</span>
                            <span>${selectedVehicle.final_fare.toFixed(2)}</span>
                        </div>
                    </div>

                    <button className="confirm-button" onClick={onConfirm}>
                        Confirm Ride
                    </button>
                </div>
            )}
        </div>
    )
}

export default VehicleResultsPanel
