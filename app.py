from flask import Flask, send_file, request, jsonify
import libtorrent as lt
import os
import time

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    magnet_uri = data.get('magnet_uri')

    if not magnet_uri:
        return jsonify({'error': 'Magnet URI is required'}), 400

    download_dir = 'downloads'
    os.makedirs(download_dir, exist_ok=True)
    ses = lt.session()
    params = {
        'save_path': download_dir,
        'storage_mode': lt.storage_mode_t.storage_sparse
    }
    handle = lt.add_magnet_uri(ses, magnet_uri, params)

    # Wait for download to complete
    print("Downloading...")
    while not handle.has_metadata():
        time.sleep(1)
    while handle.status().progress < 1.0:
        time.sleep(1)

    file_path = os.path.join(download_dir, handle.name())
    if not os.path.isfile(file_path):
        return jsonify({'error': 'Download failed'}), 500

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
