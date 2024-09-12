from flask import Flask, send_file, request, jsonify
import asyncio
import webtorrent
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
async def download():
    data = request.json
    magnet_uri = data.get('magnet_uri')
    
    if not magnet_uri:
        return jsonify({'error': 'Magnet URI is required'}), 400

    # Start downloading the file
    download_dir = 'downloads'
    os.makedirs(download_dir, exist_ok=True)
    client = webtorrent.Client()
    torrent = client.add(magnet_uri)

    # Wait until the torrent is downloaded
    while not torrent.downloaded:
        await asyncio.sleep(1)
    
    file_path = os.path.join(download_dir, torrent.files[0].name)
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
