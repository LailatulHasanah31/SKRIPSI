# Instalasi Module yang Dibutuhkan 
#pip install SpeechRecognition
#pip install Flask
#pip install Flask-SQLAlchemy
#pip install Flask Flask-Migrate
#pip install mysqlclient
#pip install flask-mysqldb



# library speech
#import speech_recognition as sr
#import pyaudio



# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
# from google.colab import drive
# drive.mount('/content/drive')
# from google.colab.output import eval_js
# print(eval_js("google.colab.kernel.proxyPort(5000)"))

app = Flask(__name__)
#app = Flask(__name__, template_folder='D:/Skripsi/templates/')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'hasanah123.'
app.config['MYSQL_DB'] = 'skripsi'
mysql = MySQL(app)

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

#@app.route('/save_audio', methods=['GET', 'POST'])
@app.route('/save_audio', methods=['POST'])
def save_audio():
    data = request.get_json()
    audio_url = data.get('audio_url')

    #new_record = AudioRecord(audio_url=audio_url)
    db = mysql.connection.cursor()
    db.execute("INSERT INTO audio_records(audio_data) VALUES (%s)", (audio_url,))
    #db.session.commit()

    
    #
    mysql.connection.commit()
    db.close()

    return jsonify({'message': 'Audio saved successfully'})

#database
        

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=False)


# Sumber:
#https://github.com/davidsproject/VRecorder
