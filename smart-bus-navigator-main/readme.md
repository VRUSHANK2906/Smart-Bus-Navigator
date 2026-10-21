# 🚌 Smart Bus Navigator

LIVE DEMO : https://smart-bus-navigator.vercel.app/

A smart bus navigation system built for **HACK4SDG**. Passengers scan a QR code printed on the back of their bus ticket to see the route, track the bus live on a map, and get an automatic alert before their stop.

## Features

- **Route visualization:** the full route and numbered stops are drawn on Google Maps.
- **Roadmap on the ticket:** a printable ticket back with the stop-by-stop roadmap and a QR code.
- **QR-based live tracking:** scanning the QR opens the live location of that specific bus.
- **Automated stop alerts:** pick your destination and get a vibration, voice message and notification when the bus is within 500 m.
- **Driver mode:** the driver's phone shares its GPS location, with a built-in simulator for demos.

## How it works

```
Driver phone (GPS) → Firebase Realtime DB → Passenger page (Google Maps)
                         buses/<bus_id>               ↑
Ticket QR code → /bus/<bus_id> ───────────────────────┘
```

1. The driver page reads GPS with `navigator.geolocation` and writes the position to Firebase.
2. The passenger page polls Firebase every 3 seconds and moves the bus marker on the map.
3. The distance from the bus to the selected stop is calculated with the haversine formula. Under 500 m, the alert fires.
4. Flask serves the pages, loads routes from `routes.json`, and generates a QR code for each bus.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (Flask) |
| Database | Firebase Realtime Database |
| Maps | Google Maps JavaScript API |
| Tracking | Browser Geolocation (GPS) |
| QR codes | `qrcode` (Python) |

## Project structure

```
smart-bus-navigator/
├── app.py              # Flask routes and QR generation
├── routes.json         # Bus routes and stops
├── requirements.txt
├── .env.example        # Environment variable template
├── templates/
│   ├── home.html       # Route list
│   ├── passenger.html  # Live map, stop alerts
│   ├── driver.html     # GPS sharing and simulator
│   └── ticket.html     # Printable ticket back
└── static/style.css
```

## Getting started

### 1. Clone and install
```bash
git clone https://github.com/YOUR_USERNAME/smart-bus-navigator.git
cd smart-bus-navigator
pip install -r requirements.txt
```

### 2. Set up Firebase
1. Create a project at the [Firebase Console](https://console.firebase.google.com).
2. Add a **Realtime Database**.
3. In the Rules tab, publish:
   ```json
   { "rules": { "buses": { ".read": true, ".write": true } } }
   ```
   These rules are for development only. See [Security notes](#security-notes).

### 3. Get a Google Maps API key
Enable the **Maps JavaScript API** in the [Google Cloud Console](https://console.cloud.google.com) and create an API key.

### 4. Configure environment variables
```bash
cp .env.example .env     # Windows: copy .env.example .env
```
```
GOOGLE_MAPS_API_KEY=your_key
FIREBASE_DB_URL=https://your-project-default-rtdb.firebaseio.com
PUBLIC_BASE_URL=http://localhost:5000
```

### 5. Run
```bash
python app.py
```
Open http://localhost:5000.

## Usage

| Page | URL | Purpose |
|---|---|---|
| Home | `/` | List of routes |
| Passenger | `/bus/bus101` | Live map and stop alerts (opened by the QR code) |
| Driver | `/driver/bus101` | Share real GPS or run the simulator |
| Ticket back | `/ticket/bus101` | Printable roadmap with QR code |
| QR image | `/qr/bus101.png` | The QR code alone |

### Demo without GPS
1. Open `/driver/bus101` and click **Simulate bus (demo)**.
2. In another window, open `/bus/bus101` and select a destination stop.
3. Watch the bus move along the route and the alert fire near your stop.

### Real GPS on a phone
Browsers only allow GPS over HTTPS. Deploy the app (for example on Render) or use a tunnel such as `ngrok http 5000`, then set `PUBLIC_BASE_URL` to the HTTPS address so the QR codes point to it.

## Adding a new route
Add an entry to `routes.json`:
```json
"bus102": {
  "name": "Route 102 - Origin to Destination",
  "stops": [
    {"name": "Stop A", "lat": 17.40, "lng": 78.40},
    {"name": "Stop B", "lat": 17.42, "lng": 78.45}
  ]
}
```

## Security notes
- The Firebase rules above allow open read/write on `buses` for development. In production, require authentication for drivers and give passengers read-only access.
- Never commit `.env`. Restrict the Google Maps key to the Maps JavaScript API and to your deployed domain.

## Future improvements
- ETA estimates using the Google Distance Matrix API
- Firebase real-time listeners instead of polling
- Authenticated driver accounts
- Multi-route search and nearby-stop suggestions
- Offline support and "last updated" indicator

## Screenshots
_Add screenshots or a short GIF of the passenger view, ticket back and stop alert here._
