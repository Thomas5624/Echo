import subprocess
from flask import Response, stream_with_context

def stream_youtube_audio(video_id):
    def generate():
        proc_yt = subprocess.Popen(
            ['yt-dlp', '-f', 'bestaudio', '-o', '-', f'https://www.youtube.com/watch?v={video_id}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        proc_ffmpeg = subprocess.Popen(
            ['ffmpeg', '-i', 'pipe:0', '-f', 'mp3', '-ab', '192000', '-vn', 'pipe:1'],
            stdin=proc_yt.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        proc_yt.stdout.close()

        while True:
            data = proc_ffmpeg.stdout.read(4096)
            if not data:
                break
            yield data

        proc_ffmpeg.stdout.close()
        proc_ffmpeg.wait()
        proc_yt.wait()

    return Response(stream_with_context(generate()), mimetype='audio/mpeg')