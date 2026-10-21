import io, json, os
from flask import Flask, render_template, jsonify, send_file, abort
import qrcode
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
with open("routes.json") as f:
    ROUTES = json.load(f)

def cfg():
    return dict(
        maps_key=os.getenv("GOOGLE_MAPS_API_KEY", ""),
        db_url=os.getenv("FIREBASE_DB_URL", "").rstrip("/"),
    )

def get_route(bus_id):
    r = ROUTES.get(bus_id)
    if not r:
        abort(404)
    return r

@app.route("/")
def home():
    return render_template("home.html", routes=ROUTES)

@app.route("/bus/<bus_id>")            # opened by scanning the ticket QR
def passenger(bus_id):
    return render_template("passenger.html", bus_id=bus_id, route=get_route(bus_id), **cfg())

@app.route("/driver/<bus_id>")         # driver phone broadcasts GPS
def driver(bus_id):
    return render_template("driver.html", bus_id=bus_id, route=get_route(bus_id), **cfg())

@app.route("/ticket/<bus_id>")         # printable back-of-ticket roadmap + QR
def ticket(bus_id):
    return render_template("ticket.html", bus_id=bus_id, route=get_route(bus_id))

@app.route("/api/route/<bus_id>")
def api_route(bus_id):
    return jsonify(get_route(bus_id))

@app.route("/qr/<bus_id>.png")
def qr(bus_id):
    get_route(bus_id)
    base = os.getenv("PUBLIC_BASE_URL", "http://localhost:5000").rstrip("/")
    img = qrcode.make(f"{base}/bus/{bus_id}")
    buf = io.BytesIO(); img.save(buf, "PNG"); buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
