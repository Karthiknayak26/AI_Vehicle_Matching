import { useState } from 'react'
import { getLocationNames } from '../utils/geocoding'
import './RidePlanningCard.css'

function RidePlanningCard({ onSearch }) {
    const [pickup, setPickup] = useState('')
    const [drop, setDrop] = useState('')
    const locations = getLocationNames()

    const handleSubmit = (e) => {
        e.preventDefault()

        if (!pickup || !drop) {
            alert('Please select both pickup and drop locations')
            return
        }

        if (pickup === drop) {
            alert('Pickup and drop locations must be different')
            return
        }

        onSearch(pickup, drop, 'balanced')
    }

    return (
        <div className="ride-planning-card glass fade-in">
            <div className="card-header">
                <h1>🚗 AI Ride Matching</h1>
                <p>Premium vehicle matching powered by machine learning</p>
            </div>

            <form onSubmit={handleSubmit} className="ride-form">
                <div className="form-group">
                    <label htmlFor="pickup">
                        <span className="icon">📍</span>
                        Pickup Location
                    </label>
                    <select
                        id="pickup"
                        value={pickup}
                        onChange={(e) => setPickup(e.target.value)}
                        required
                    >
                        <option value="">Select pickup location</option>
                        {locations.map(loc => (
                            <option key={loc} value={loc}>{loc}</option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="drop">
                        <span className="icon">🎯</span>
                        Drop Location
                    </label>
                    <select
                        id="drop"
                        value={drop}
                        onChange={(e) => setDrop(e.target.value)}
                        required
                    >
                        <option value="">Select drop location</option>
                        {locations.map(loc => (
                            <option key={loc} value={loc}>{loc}</option>
                        ))}
                    </select>
                </div>

                <button type="submit" className="search-button">
                    Find Rides
                </button>
            </form>

            <div className="card-footer">
                <small>🤖 Powered by AI • 🔒 Secure • ⚡ Real-time</small>
            </div>
        </div>
    )
}

export default RidePlanningCard
