// Mock geocoding - predefined Udupi, India locations
export const LOCATIONS = {
    "Malpe Beach": { lat: 13.3500, lon: 74.7042, name: "Malpe Beach" },
    "Udupi Sri Krishna Temple": { lat: 13.3409, lon: 74.7421, name: "Udupi Sri Krishna Temple" },
    "Manipal University": { lat: 13.3467, lon: 74.7926, name: "Manipal University" },
    "Kaup Beach": { lat: 13.2333, lon: 74.7500, name: "Kaup Beach" },
    "St. Mary's Island": { lat: 13.3667, lon: 74.6833, name: "St. Mary's Island" },
    "Udupi Bus Stand": { lat: 13.3356, lon: 74.7467, name: "Udupi Bus Stand" },
    "Manipal Hospital": { lat: 13.3500, lon: 74.7833, name: "Manipal Hospital" },
    "Udupi Railway Station": { lat: 13.3333, lon: 74.7500, name: "Udupi Railway Station" },
    "Kadiyali": { lat: 13.3100, lon: 74.7300, name: "Kadiyali" },
    "Kalsanka": { lat: 13.3200, lon: 74.7200, name: "Kalsanka" },
    "Ambalpady": { lat: 13.3450, lon: 74.7550, name: "Ambalpady" },
    "Parkala": { lat: 13.3600, lon: 74.7400, name: "Parkala" },
    "Manipal End Point": { lat: 13.3533, lon: 74.7967, name: "Manipal End Point" },
    "Udupi Market": { lat: 13.3389, lon: 74.7456, name: "Udupi Market" },
    "Brahmavar": { lat: 13.3700, lon: 74.7100, name: "Brahmavar" }
}

export function geocode(locationName) {
    const coords = LOCATIONS[locationName]

    if (!coords) {
        // Random jitter within Udupi bounds if location not found
        return {
            lat: 13.3409 + (Math.random() - 0.5) * 0.05,
            lon: 74.7421 + (Math.random() - 0.5) * 0.05,
            name: locationName
        }
    }

    return coords
}

export function getLocationNames() {
    return Object.keys(LOCATIONS)
}
