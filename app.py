# Instalasi Module yang Dibutuhkan 
#pip install SpeechRecognition
#pip install Flask
#pip install Flask-SQLAlchemy
#pip install Flask Flask-Migrate
#pip install mysqlclient



# library speech
#import speech_recognition as sr
#import pyaudio



# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from google.colab import drive
# drive.mount('/content/drive')
# from google.colab.output import eval_js
# print(eval_js("google.colab.kernel.proxyPort(5000)"))

app = Flask(__name__)
#app = Flask(__name__, template_folder='D:/Skripsi/templates/')


#route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/js/<path:filename>')
def serve_static(filename):
    return send_from_directory('static/js', filename)

@app.route('/speech_render')
def speech_render():
    return render_template('speech.html')

@app.route('/save_audio', methods=['POST'])
def save_audio():
    data = request.get_json()
    audio_url = data.get('audio_url')

    new_record = AudioRecord(audio_url=audio_url)
    db.session.add(new_record)
    db.session.commit()

    return jsonify({'message': 'Audio saved successfully'})

#database
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://root:hasanah123.@localhost/skripsi'  # Ganti dengan URL database yang sesuai
db.init_app(app)
class AudioRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audio_url = db.Column(db.String(100), nullable=False)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=False)


# Sumber:
#https://github.com/davidsproject/VRecorder
