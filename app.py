from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Server is running'

@app.route('/download', methods=['GET'])
def download():
    magnet_uri = request.args.get('magnet')
    if not magnet_uri:
        return jsonify({"error": "Magnet link is required."}), 400

    # For demonstration purposes, we'll return a placeholder response.
    # Implement torrent handling here using a library like `webtorrent` if needed.
    return jsonify({"message": f"Downloading from {magnet_uri}"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
