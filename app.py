
import os
import socket
from flask import Flask, request, send_from_directory, redirect, url_for, render_template, flash, session

UPLOAD_FOLDER = 'uploads'
SHARED_FOLDER = 'shared'
ALLOWED_EXTENSIONS = set([
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',
    'zip', 'apk', 'mp4', 'mp3', 'doc', 'docx',
    'ppt', 'pptx', 'xls', 'xlsx', 'csv', 'webm',
    'avi', 'mkv', 'html', 'css', 'js', 'py', 'java',
    'c', 'cpp', 'ts', 'json', 'xml', 'php', 'sql'
])

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SHARED_FOLDER'] = SHARED_FOLDER
PASSWORD = '1234'

# Create folders if missing
for folder in [UPLOAD_FOLDER, SHARED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash("Incorrect password.")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'files' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files')
        for file in files:
            if file and allowed_file(file.filename):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
        flash('Files uploaded successfully')
        return redirect(url_for('index'))

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash(f'{filename} deleted successfully')
    return redirect(url_for('index'))

@app.route('/text', methods=['GET', 'POST'])
def text_input():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    text_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'text.html')
    if not os.path.exists(text_file_path):
        with open(text_file_path, 'w') as f:
            f.write('')

    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            with open(text_file_path, "a") as f:
                f.write(text + "\n")
            flash("Text saved to text.html")
            return redirect(url_for('text_input'))

    with open(text_file_path, 'r') as f:
        text_lines = f.readlines()

    return render_template('text.html', text_lines=text_lines)

@app.route('/shared')
def shared_files():
    files = os.listdir(SHARED_FOLDER)
    return render_template('shared.html', files=files)

@app.route('/shared/download/<filename>')
def shared_download(filename):
    return send_from_directory(SHARED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    print(f"Server running on http://{get_ip()}:8000")
    app.run(host='0.0.0.0', port=8000)
