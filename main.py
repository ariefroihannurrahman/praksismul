from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''
        <h1>Sistem Multimedia</h1>
        <form method="POST" action="/audio" enctype="multipart/form-data">
            <label for="file">Audio Compression : </label>
            <input type="file" id="file" name="file">
            <button type="submit">Compress</button>
        </form>
        <form method="POST" action="/image" enctype="multipart/form-data">
            <label for="file">Image Compression : </label>
            <input type="file" id="file" name="file">
            <button type="submit">Compress</button>
        </form>
    '''

@app.route('/audio', methods=['GET', 'POST'])
def audio_compression():
    if request.method == 'GET':
        return 'GET Success'
    if request.method == 'POST':
        file = request.files['file']
        file_name = secure_filename(file.filename)
        if file:
            audio_io = io.BytesIO()
            audio = AudioSegment.from_file(file)
            audio.export(audio_io, format="mp3", bitrate='64k')
            return send_file(
                audio_io,
                as_attachment=True,
                download_name=f'compressed_{file_name}',
                mimetype="audio/mp3"
            )
        else:
            return '''
                <h1>File Not Found</h1>
            '''
    else:
            return '''
                <h1>Unknown Method</h1>
            '''

@app.route('/image', methods=['GET', 'POST'])
def image_compression():
    if request.method == 'GET':
        return 'GET Success'
    if request.method == 'POST':
        file = request.files['file']
        file_name = secure_filename(file.filename)
        if file:
            img = Image.open(file)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
                img_io = io.BytesIO()
                img.save(img_io, format='JPEG', optimize=True, quality=75)
                img_io.seek(0)
                return send_file(
                    img_io,
                    as_attachment=True,
                    download_name=f'compressed_{file_name}',
                    mimetype='image/jpeg'
                )
            else:
                return '''
                    <h1>Use Image Mode RGBA</h1>
                '''
        else:
            return '''
                <h1>File Not Found</h1>
            '''
    else:
            return '''
                <h1>Unknown Method</h1>
            '''

if __name__ == '__main__':
    app.run(port=8080)
