import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import { createTrafficRoute, simulateTraffic, getTrafficColor } from '../utils/traffic'
import './MapContainer.css'

// Fix for default marker icons in Leaflet with Vite
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

function MapContainer({ pickup, drop, showRoute, vehicles, animatingVehicle, selectedVehicle }) {
    const mapRef = useRef(null)
    const mapInstanceRef = useRef(null)
    const markersRef = useRef([])
    const routeLayersRef = useRef([])
    const vehicleMarkersRef = useRef([])
    const [vehiclePosition, setVehiclePosition] = useState(null)

    useEffect(() => {
        // Initialize map
        if (!mapInstanceRef.current) {
            mapInstanceRef.current = L.map(mapRef.current, {
                center: [13.3409, 74.7421], // Udupi Sri Krishna Temple
                zoom: 13,
                zoomControl: true,
                attributionControl: false
            })

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
            }).addTo(mapInstanceRef.current)
        }

        return () => {
            // Cleanup on unmount
            if (mapInstanceRef.current) {
                mapInstanceRef.current.remove()
                mapInstanceRef.current = null
            }
        }
    }, [])

    // Animation effect for moving vehicle
    useEffect(() => {
        if (!animatingVehicle) {
            setVehiclePosition(null)
            return
        }

        const animate = () => {
            const now = Date.now()
            const elapsed = now - animatingVehicle.startTime
            const progress = Math.min(elapsed / animatingVehicle.duration, 1)

            // Linear interpolation
            const currentLat = animatingVehicle.startLat +
                (animatingVehicle.endLat - animatingVehicle.startLat) * progress
            const currentLon = animatingVehicle.startLon +
                (animatingVehicle.endLon - animatingVehicle.startLon) * progress

            setVehiclePosition({ lat: currentLat, lon: currentLon })

            if (progress < 1) {
                requestAnimationFrame(animate)
            }
        }

        requestAnimationFrame(animate)
    }, [animatingVehicle])

    useEffect(() => {
        if (!mapInstanceRef.current) return

        // Clear existing markers
        markersRef.current.forEach(marker => marker.remove())
        markersRef.current = []

        // Clear existing route layers
        routeLayersRef.current.forEach(layer => layer.remove())
        routeLayersRef.current = []

        // Add pickup marker
        if (pickup) {
            const pickupIcon = L.divIcon({
                className: 'custom-marker pickup-marker',
                html: '<div class="marker-pin">📍</div>',
                iconSize: [40, 40],
                iconAnchor: [20, 40]
            })

            const pickupMarker = L.marker([pickup.lat, pickup.lon], { icon: pickupIcon })
                .addTo(mapInstanceRef.current)
                .bindPopup(`<b>Pickup</b><br/>${pickup.name || 'Selected Location'}`)

            markersRef.current.push(pickupMarker)
        }

        // Add drop marker
        if (drop) {
            const dropIcon = L.divIcon({
                className: 'custom-marker drop-marker',
                html: '<div class="marker-pin">🎯</div>',
                iconSize: [40, 40],
                iconAnchor: [20, 40]
            })

            const dropMarker = L.marker([drop.lat, drop.lon], { icon: dropIcon })
                .addTo(mapInstanceRef.current)
                .bindPopup(`<b>Drop</b><br/>${drop.name || 'Selected Location'}`)

            markersRef.current.push(dropMarker)
        }

        // Clear existing vehicle markers
        vehicleMarkersRef.current.forEach(marker => marker.remove())
        vehicleMarkersRef.current = []

        // Add vehicle markers (when results are shown)
        if (vehicles && vehicles.length > 0 && pickup) {
            // Mock vehicle positions around pickup location
            const vehiclePositions = [
                { lat: pickup.lat + 0.01, lon: pickup.lon - 0.01 },
                { lat: pickup.lat - 0.01, lon: pickup.lon + 0.01 },
                { lat: pickup.lat + 0.005, lon: pickup.lon + 0.005 },
                { lat: pickup.lat - 0.005, lon: pickup.lon - 0.005 },
                { lat: pickup.lat + 0.008, lon: pickup.lon - 0.008 },
            ]

            vehicles.forEach((vehicle, idx) => {
                const pos = vehiclePositions[idx % vehiclePositions.length]

                // Choose emoji based on vehicle type
                const vehicleEmoji = vehicle.vehicle_type === 'suv' ? '🚙' :
                    vehicle.vehicle_type === 'sedan' ? '🚗' : '🚕'

                const vehicleIcon = L.divIcon({
                    html: `<div class="vehicle-marker-emoji">${vehicleEmoji}</div>`,
                    className: 'vehicle-marker',
                    iconSize: [30, 30],
                    iconAnchor: [15, 15]
                })

                const vehicleMarker = L.marker([pos.lat, pos.lon], { icon: vehicleIcon })
                    .addTo(mapInstanceRef.current)
                    .bindPopup(`
                        <b>${vehicle.vehicle_type.toUpperCase()}</b><br/>
                        ETA: ${vehicle.eta_pickup.toFixed(1)} min<br/>
                        Price: $${vehicle.final_fare.toFixed(2)}<br/>
                        AI Score: ${(vehicle.score * 100).toFixed(0)}
                    `)

                vehicleMarkersRef.current.push(vehicleMarker)
            })
        }

        // Add animated vehicle marker (after confirmation)
        if (vehiclePosition && selectedVehicle) {
            const vehicleEmoji = selectedVehicle.vehicle_type === 'suv' ? '🚙' :
                selectedVehicle.vehicle_type === 'sedan' ? '🚗' : '🚕'

            const animatedIcon = L.divIcon({
                html: `<div class="animated-vehicle-marker">${vehicleEmoji}</div>`,
                className: 'animated-vehicle',
                iconSize: [40, 40],
                iconAnchor: [20, 20]
            })

            const animatedMarker = L.marker([vehiclePosition.lat, vehiclePosition.lon], { icon: animatedIcon })
                .addTo(mapInstanceRef.current)
                .bindPopup(`
                    <b>Your Ride is Coming!</b><br/>
                    Driver arriving soon...
                `)

            vehicleMarkersRef.current.push(animatedMarker)
        }

        // Draw traffic route
        if (showRoute && pickup && drop) {
            const route = createTrafficRoute(pickup, drop, 5)
            const trafficColors = simulateTraffic(route)

            trafficColors.forEach((color, i) => {
                const polyline = L.polyline(
                    [route[i], route[i + 1]],
                    {
                        color: getTrafficColor(color),
                        weight: 6,
                        opacity: 0.8,
                        className: 'traffic-segment'
                    }
                ).addTo(mapInstanceRef.current)

                routeLayersRef.current.push(polyline)
            })

            // Fit bounds to show entire route
            const bounds = L.latLngBounds([
                [pickup.lat, pickup.lon],
                [drop.lat, drop.lon]
            ])
            mapInstanceRef.current.fitBounds(bounds, { padding: [50, 50] })
        } else if (pickup) {
            // Center on pickup if no route
            mapInstanceRef.current.setView([pickup.lat, pickup.lon], 14)
        }
    }, [pickup, drop, showRoute, vehicles, vehiclePosition, selectedVehicle])

    return <div ref={mapRef} className="map-container" />
}

export default MapContainer
