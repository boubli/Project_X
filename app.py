import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define a directory where uploaded log files will be stored
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Use an absolute path
ALLOWED_EXTENSIONS = {'txt', 'log', 'xml', 'json'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy log data for demonstration (replace with actual log data loading)
logs = [
    {"timestamp": "2023-09-19T12:34:56", "level": "INFO", "message": "Log message 1", "error_code": None},
    {"timestamp": "2023-09-19T12:35:00", "level": "ERROR", "message": "Log message 2", "error_code": 500},
]

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html', logs=logs)

# Route for uploading log files
@app.route('/upload_logs', methods=['POST'])
def upload_logs():
    # Check if a file was uploaded
    if 'log_file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['log_file']

    # Check if the file has a valid extension
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Use an absolute path to the 'uploads' directory
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File uploaded successfully')
    else:
        flash('Invalid file format. Allowed formats: txt, log, xml, json')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'  # Change this to a secret key
    app.run(debug=True)
