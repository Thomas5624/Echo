import os
import re
from flask import Response, request, jsonify

def stream_audio(path):
    range_header = request.headers.get('Range', None)
    if not os.path.exists(path):
        return jsonify({'error': 'File non trovato'}), 404

    file_size = os.path.getsize(path)
    byte1, byte2 = 0, None

    if range_header:
        match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        if match:
            byte1 = int(match.group(1))
            if match.group(2):
                byte2 = int(match.group(2))

    byte2 = byte2 or file_size - 1
    length = byte2 - byte1 + 1

    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data, 206, mimetype='audio/mpeg', direct_passthrough=True)
    rv.headers.add('Content-Range', f'bytes {byte1}-{byte2}/{file_size}')
    rv.headers.add('Accept-Ranges', 'bytes')
    rv.headers.add('Content-Length', str(length))
    return rv