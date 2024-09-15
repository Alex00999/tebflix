import json
import os

from flask import Flask, render_template, send_from_directory, abort
from werkzeug.exceptions import NotFound
import json

app = Flask(__name__)

with open("content/series.json", "r") as read_file:
    tebnev_curse_original = json.load(read_file)

with open("content/films.json", "r") as read_file:
    directors_cut = json.load(read_file)
print(tebnev_curse_original)


@app.route('/')
def index():
    return render_template('index.html', films=tebnev_curse_original, title=' - Главная')


@app.route('/watch/<content>')
def player(content):
    player_data = tebnev_curse_original | directors_cut
    return render_template('player.html', film=content, title=f' - {player_data[content]["title"]}')


@app.route('/media')
def media():
    return 'в разработке'


@app.route('/wiki')
def wiki():
    return 'в разработке'


@app.route('/images/<path:filename>')
def serve_image(filename):
    base_dir = 'static/images'
    file_path = os.path.join(base_dir, filename)

    if os.path.exists(file_path):
        return send_from_directory(base_dir, filename)
    else:
        try:
            return send_from_directory('static', 'logo.png')
        except NotFound:
            abort(404)


@app.route('/videos/<path:filename>')
def serve_video(filename):
    base_dir = 'videos'  # Папка для видео находится в корневом каталоге
    file_path = os.path.join(base_dir, filename)

    if os.path.exists(file_path):
        return send_from_directory(base_dir, filename)
    else:
        # Путь к логотипу (может быть изменен, если логотип хранится в другой папке)
        logo_path = os.path.join('static', 'logo.png')
        if os.path.exists(logo_path):
            return send_from_directory('static', 'logo.png')
        else:
            abort(404)


if __name__ == '__main__':
    app.run(port=9999)
