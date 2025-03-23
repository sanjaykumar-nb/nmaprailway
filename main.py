from flask import Flask, request, jsonify
import nmap

app = Flask(__name__)

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
    app.run(host='0.0.0.0', port=5000)
