from flask import Flask, request, jsonify
import nmap
import threading
import time

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
        nm.scan(target, arguments='-F')  # Quick scan with top 100 ports
        scan_results = nm.csv()  # Get the scan results in CSV format
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"target": target, "scan_result": scan_results})

if __name__ == '__main__':
    # Start Keep-Alive Thread
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
