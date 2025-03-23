from flask import Flask, request, jsonify
import nmap
import threading
import time
from gunicorn.app.base import BaseApplication

app = Flask(__name__)

# Keep-Alive Function to Prevent Railway from Sleeping
def keep_alive():
    while True:
        try:
            print("Keeping API alive...")
            time.sleep(300)  # Every 5 minutes
        except Exception as e:
            print(f"Error in Keep-Alive: {e}")

@app.route('/')
def home():
    return jsonify({"message": "Nmap API is running!"})

@app.route('/scan', methods=['GET'])
def scan():
    target = request.args.get('target')
    if not target:
        return jsonify({"error": "No target provided!"}), 400

    nm = nmap.PortScanner()

    try:
        nm.scan(target, arguments='-T4 --top-ports 10')  # Optimized for fast scanning
        scan_results = nm.csv()  # Get results in CSV format
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"target": target, "scan_result": scan_results})

# Gunicorn Class for Stable Deployment
class FlaskApp(BaseApplication):
    def __init__(self, app, options=None):
        self.app = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return app

if __name__ == "__main__":
    # Start Keep-Alive Thread
    threading.Thread(target=keep_alive, daemon=True).start()

    # Start Gunicorn Server
    options = {"bind": "0.0.0.0:5000", "workers": 1}
    FlaskApp(app, options).run()
