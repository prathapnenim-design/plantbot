import threading
import time
import random
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_data = {
    "soil": 60,
    "water": 55,
    "ph": 6.5,
    "n": 40,
    "p": 35,
    "k": 45,
    "temp": 25,
    "hum": 60
}

def generate_fake_data():
    global latest_data
    while True:
        latest_data["soil"] = random.randint(45, 75)
        latest_data["water"] = random.randint(40, 70)
        latest_data["ph"] = round(random.uniform(6.0, 7.5), 1)
        latest_data["n"] = random.randint(30, 60)
        latest_data["p"] = random.randint(30, 60)
        latest_data["k"] = random.randint(30, 60)
        latest_data["temp"] = round(random.uniform(24.0, 30.0), 1)
        latest_data["hum"] = random.randint(50, 75)

        print("📟 CLOUD DATA:", latest_data)
        time.sleep(3)

@app.route("/api/sensors", methods=["GET"])
def get_sensors():
    return jsonify({
        "soilPercent": latest_data["soil"],
        "waterPercent": latest_data["water"],
        "phValue": latest_data["ph"],
        "nitrogen": latest_data["n"],
        "phosphorus": latest_data["p"],
        "potassium": latest_data["k"],
        "temperature": latest_data["temp"],
        "humidity": latest_data["hum"]
    })

@app.route("/health")
def health():
    return jsonify({"status": "online", "mode": "cloud-simulated"})

if __name__ == "__main__":
    data_thread = threading.Thread(target=generate_fake_data, daemon=True)
    data_thread.start()
    app.run(host="0.0.0.0", port=5000)
