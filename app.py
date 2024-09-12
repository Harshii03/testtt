from flask import Flask, request, jsonify, send_from_directory
import libtorrent as lt
import os
import time

app = Flask(__name__)
download_dir = './downloads'

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Initialize session
session = lt.session()
session.listen_on(6881, 6891)

@app.route('/')
def home():
    return 'Server is running'

@app.route('/download', methods=['GET'])
def download():
    magnet_uri = request.args.get('magnet')
    if not magnet_uri:
        return jsonify({"error": "Magnet link is required."}), 400

    # Add the torrent to the session
    params = {
        'save_path': download_dir,
        'storage_mode': lt.storage_mode_t.storage_mode_sparse
    }
    handle = lt.add_magnet_uri(session, magnet_uri, params)

    # Wait for the torrent to start downloading
    print("Waiting for torrent metadata...")
    while not handle.has_metadata():
        time.sleep(1)

    print("Torrent metadata available. Starting download...")
    torrent_info = handle.get_torrent_info()
    file_info = next((f for f in torrent_info.files() if f.path().endswith('.mp4')), None)

    if file_info:
        file_name = file_info.path()
        download_link = f'/downloads/{file_name}'
        return jsonify({"message": f"Download your video here: <a href='{download_link}'>{download_link}</a>"})
    else:
        return jsonify({"message": "No video file found in the torrent."})

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(download_dir, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
