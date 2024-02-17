# Instalasi Module yang Dibutuhkan 
#pip install SpeechRecognition
#pip install Flask
#pip install Flask-SQLAlchemy
#pip install Flask Flask-Migrate
#pip install mysqlclient
#pip install flask-mysqldb
#pip install openai



# library speech
import speech_recognition as sr
import os
# import moviepy.editor as moviepy
from moviepy.editor import AudioFileClip
# import requests
# import base64
# from pydub import AudioSegment
# import logging
#import pyaudio

#library chatgpt
from openai import OpenAI


# app.py
from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
# from werkzeug.utils import secure_filename
# from flask_mysqldb import MySQL
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
# from google.colab import drive
# drive.mount('/content/drive')
# from google.colab.output import eval_js
# print(eval_js("google.colab.kernel.proxyPort(5000)"))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/audio'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Contoh: 16 MB

# UPLOAD_FOLDER = 'static/audio'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app = Flask(__name__, template_folder='D:/Skripsi/templates/')

counter_file_path = 'counter.txt'
if os.path.exists(counter_file_path):
    with open(counter_file_path, 'r') as f:
        fileCounter = f.read()

# Menyimpan nilai yang telah diincrement ke dalam file counter.txt
with open(counter_file_path, 'w') as f:
    files = os.listdir('static/audio')
    fileCounter = len(files)/2
    fileCounter += 1 
    f.write(str(fileCounter))

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'hasanah123.'
# app.config['MYSQL_DB'] = 'skripsi'
# mysql = MySQL(app)

#route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/static/js/<path:filename>')
def serve_static(filename):
    return send_from_directory('static/js', filename)

@app.route('/speech_render')
def speech_render():
    return render_template('speech.html')

# @app.route('/download')
# def download():
#     filename = f'audio_{fileCounter}.webm'
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/record', methods=['POST'])
def record_file():
    global fileCounter  # Gunakan variabel global

    if 'audioBlob' not in request.files:
        return 'No audioBlob in the request'

    file = request.files['audioBlob']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = f'audio_{fileCounter}.webm'
        # file.seek(0)
        # filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # file.flush()
        file.close()
        
        
        fileCounter += 1  # Increment urutan file
        return f'Audio berhasil diunggah dengan nama {filename}'

    # # Langkah 1: Mengenali ucapan
    # recognizer = sr.Recognizer()

    # # Menggunakan 'audio_url' sebagai URL file audio
    # audio_file = sr.AudioFile(audio_url)

    # with audio_file as source:
    #     recognizer.adjust_for_ambient_noise(source)
    #     audio = recognizer.record(source)

    # try:
    #     input_text = recognizer.recognize_google(audio, language='in-ID')  # Ganti dengan kode bahasa yang sesuai
    #     print('Speech Recognition Result:', input_text)
    # except sr.UnknownValueError:
    #     print('Speech Recognition could not understand audio')
    #     return jsonify({'message': 'Speech Recognition could not understand audio'})
    # except sr.RequestError as e:
    #     print(f'Speech Recognition request failed: {e}')
    #     return jsonify({'message': 'Speech Recognition request failed'})

    #Menyimpan audio ke database
    # db = mysql.connection.cursor()
    # db.execute("INSERT INTO audio_records(audio_data, description) VALUES (%s, %s)", (audio_url, input_text))
    # mysql.connection.commit()
    # db.close()


#database
@app.route('/upload_render')
def upload_render():
    return render_template('upload.html')        

@app.route('/upload', methods=['POST'])
def upload():
    # global fileCounter

    if 'suara' not in request.files:
        return redirect(request.url)

    file = request.files['suara']

    if file.filename == '' or not file.filename.endswith('.mp3'):
        return redirect(request.url)

    filename = f'audio_{fileCounter}.mp3'
    #     # file.seek(0)
    #     # filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # audio = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), format="webm")
    # audio.export(os.path.join(app.config['UPLOAD_FOLDER'], filename_wav), format="wav")
    
    return render_template('upload.html', message='Suara berhasil diunggah!')


@app.route('/konversi', methods=['POST'])
def konversi():
    global fileCounter
    filename = f'audio_{fileCounter}.mp3'
    filename_wav = f'audio_{fileCounter}.wav'

    # Path ke file input di folder static/audio
    input_file_path = os.path.join('static', 'audio', filename)

    # Path untuk menyimpan file output di folder static/audio
    output_file_path = os.path.join('static', 'audio', filename_wav)

    # Memastikan file input ada sebelum membuat objek VideoFileClip
    if not os.path.exists(input_file_path):
        return 'File input tidak ditemukan'

    # Membuat objek VideoFileClip
    # clip = moviepy.VideoFileClip(input_file_path)
    clip = AudioFileClip(input_file_path)

    # Menyimpan file audio ke format wav di folder static/audio
    # clip.audio.write_audiofile(output_file_path)
    clip.write_audiofile(output_file_path, codec='pcm_s16le')
    return render_template('upload.html', message2='File berhasil dikonversi')


@app.route('/extract', methods=['POST'])
def extract():
    global fileCounter
    filename_wav = f'audio_{fileCounter}.wav'

    # Path untuk menyimpan file output di folder static/audio
    input = os.path.join('static', 'audio', filename_wav)

    # Memastikan file input ada sebelum membuat objek VideoFileClip
    if not os.path.exists(input):
        return 'File input tidak ditemukan'
    
     # Langkah 1: Mengenali ucapan
    recognizer = sr.Recognizer()

    # Menggunakan 'audio_url' sebagai URL file audio
    audio_file = sr.AudioFile(input)

    with audio_file as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

    try:
        input_text = recognizer.recognize_google(audio, language='in-ID')  # Ganti dengan kode bahasa yang sesuai
        print('Speech Recognition Result:', input_text)
    except sr.UnknownValueError:
        print('Speech Recognition could not understand audio')
        return jsonify({'message': 'Speech Recognition could not understand audio'})
    except sr.RequestError as e:
        print(f'Speech Recognition request failed: {e}')
        return jsonify({'message': 'Speech Recognition request failed'})
    
    
    #client = OpenAI()
    client = OpenAI(api_key='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')
    #input_text = "Namaku Hasanah aku punya adik bernama ani dan budi ani berumur 9 tahun sedangkan budi berumur 12 tahun"

    system_prompt = """Tugas kamu adalah bertindak sebagai pengekstrak teks. User akan memberi kamu teks didalam triple backticks. 
                    Dan tugas kamu untuk mencari dan mengembalikan 
                    nama bisa diperbaiki dengan melihat ejaan nama, 
                    umur kalau sekarang tanggal 2 Februari 2024(dalam bentuk integer penghitungan dengan teknik flooring), 
                    jenis kelamin, 
                    agama, 
                    nik harus 16 digit kalau ada angka yang terpisah gabungkan saja, 
                    tanggal lahir, 
                    tempat lahir, 
                    dan kewarganegaraan 
                    dari teks tersebut."""
    # Panggil API OpenAI untuk mendapatkan respons
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"```{input_text}```"}
    ])

    # Ekstrak nama dan umur dari respons
    extracted_data = completion.choices[0].message.content
    #print(completion)
    # Pisahkan nama dan umur (contoh sederhana)
    #nama = extracted_data.split("Nama")[1].strip()

    # Tampilkan hasil ekstraksi data
    print(extracted_data)

    data_lines = extracted_data.split('\n')

    # Inisialisasi variabel
    nama = None
    umur = None
    jenis_kelamin = None
    agama = None
    nik = None
    tanggal_lahir = None
    tempat_lahir = None
    kewarganegaraan = None

    # Iterasi melalui setiap baris data dan ekstrak informasi yang diperlukan
    for line in data_lines:
        if 'Nama:' in line:
            nama = line.split(':')[1].strip()
        elif 'Umur:' in line:
            umur = line.split(':')[1].strip()
        elif 'Jenis kelamin:' in line or 'Jenis Kelamin:' in line:
            jenis_kelamin = line.split(':')[1].strip()
        elif 'Agama:' in line:
            agama = line.split(':')[1].strip()
        elif 'NIK:' in line:
            nik = line.split(':')[1].strip()
        elif 'Tanggal lahir:' in line or 'Tanggal Lahir:' in line:
            tanggal_lahir = line.split(':')[1].strip()
        elif 'Tempat lahir:' in line or 'Tempat Lahir:' in line:
            tempat_lahir = line.split(':')[1].strip()
        elif 'Kewarganegaraan:' in line:
            kewarganegaraan = line.split(':')[1].strip()

    # fileCounter += 1 
    # Tampilkan hasil ekstraksi data
    print(nama)
    print(umur)
    print(jenis_kelamin)
    print(agama)
    print(nik)
    print(tanggal_lahir)
    print(tempat_lahir)
    print(kewarganegaraan)
    return render_template('upload.html', 
                           filename_wav = filename_wav,
                           message3=input_text,
                           extracted_data=extracted_data,
                           nama=nama,
                           umur=umur,
                           jenis_kelamin=jenis_kelamin,
                           agama=agama,
                           nik=nik,
                           tanggal_lahir=tanggal_lahir,
                           tempat_lahir=tempat_lahir,
                           kewarganegaraan=kewarganegaraan
                          )

@app.route('/simpan', methods=['POST'])
def simpan():
    global fileCounter
    fileCounter += 1 
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False)


# Sumber:
#https://github.com/davidsproject/VRecorder
