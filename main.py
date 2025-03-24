from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/scan', methods=['GET'])
def scan():
    target = request.args.get('target')
    if not target:
        return jsonify({"error": "No target provided"}), 400

    result = subprocess.run(["nmap", target], capture_output=True, text=True)
    return jsonify({"result": result.stdout})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
