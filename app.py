from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from main import generate_ebook
import re

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    title = request.form['title']
    print(f"Generating eBook with title: {title}")
    generate_ebook(title, BASE_DIR)
    return redirect(url_for('result', title=title))

@app.route('/result')
def result():
    title = request.args.get('title')
    sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", title)
    pdf_path = f"{sanitized_title}.pdf"
    mp3_path = f"{sanitized_title}.mp3"
    print(f"PDF Path: {pdf_path}, MP3 Path: {mp3_path}")
    return render_template('result.html', title=title, pdf_path=pdf_path, mp3_path=mp3_path)

@app.route('/download/<filename>')
def download(filename):
    print(f"Downloading file: {filename}")
    return send_from_directory(BASE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)