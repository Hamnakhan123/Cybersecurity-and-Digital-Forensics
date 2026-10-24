// Geolocation logic with a mock navigator.geolocation, so success and every error code can be seen.
const LAB = { lat: 24.8607, lon: 67.0011 };            // example point in Karachi

function distanceKm(a, b) {                              // haversine great-circle distance
  const R = 6371, rad = d => d * Math.PI / 180;
  const dLat = rad(b.lat - a.lat), dLon = rad(b.lon - a.lon);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(h));
}

// Mock that behaves like the browser API: async, success callback or error callback
function mockGeolocation(scenario) {
  return {
    getCurrentPosition(success, error, options) {
      setTimeout(() => {
        if (scenario.code) error({ code: scenario.code, message: scenario.msg });
        else success({ coords: { latitude: scenario.lat, longitude: scenario.lon, accuracy: scenario.acc }, timestamp: 0 });
      }, 1);
    },
  };
}

const scenarios = [
  { name: "student in the lab", lat: 24.8611, lon: 67.0015, acc: 15 },
  { name: "student at the airport", lat: 24.9065, lon: 67.1608, acc: 30 },
  { name: "user clicked Block", code: 1, msg: "User denied Geolocation" },
  { name: "no GPS/Wi-Fi fix", code: 2, msg: "Position unavailable" },
  { name: "took too long", code: 3, msg: "Timeout expired" },
];
const reasons = { 1: "PERMISSION_DENIED", 2: "POSITION_UNAVAILABLE", 3: "TIMEOUT" };

(async () => {
  for (const sc of scenarios) {
    await new Promise(done => {
      mockGeolocation(sc).getCurrentPosition(
        pos => {
          const me = { lat: pos.coords.latitude, lon: pos.coords.longitude };
          const d = distanceKm(me, LAB);
          console.log(`${sc.name.padEnd(24)} ${d.toFixed(2).padStart(6)} km  accuracy ±${pos.coords.accuracy} m  -> ${d <= 0.5 ? "checked in" : "too far"}`);
          done();
        },
        err => { console.log(`${sc.name.padEnd(24)} error ${err.code} ${reasons[err.code]}`); done(); },
        { timeout: 10000 }
      );
    });
  }
  // Privacy: reduce precision before storing or sharing
  const exact = { lat: 24.861143, lon: 67.001522 };
  for (const places of [6, 3, 2, 1]) {
    console.log(`round to ${places} dp: ${exact.lat.toFixed(places)}, ${exact.lon.toFixed(places)}  (~${(111000 / 10 ** places).toFixed(places > 3 ? 2 : 0)} m precision)`);
  }
})();
