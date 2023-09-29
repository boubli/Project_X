from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Define global variables
filtered_results = []

# Define routes and functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    global filtered_results  # Use the global filtered_results list
    filtered_results = []  # Clear the previous results

    # Retrieve search parameters from the form
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    keyword = request.form.get('keyword')

    # Get the uploaded log file
    uploaded_file = request.files['log_file']

    # Check if a file was uploaded
    if uploaded_file:
        # Save the uploaded file to a temporary location
        log_file_path = 'uploads/' + uploaded_file.filename
        uploaded_file.save(log_file_path)
    else:
        return "No log file uploaded."

    try:
        # Open and read the log file
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                # Split the log entry into parts (assuming space-separated)
                parts = line.strip().split(' ')
                if len(parts) >= 3:
                    timestamp, log_level, message = parts[0], parts[1], ' '.join(parts[2:])

                    # Check if the timestamp falls within the date range
                    # You may need to convert timestamp to a datetime object and compare here
                    # Example: timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    # Filter by start_date and end_date

                    # Check if the keyword exists in the log message
                    if keyword.lower() in message.lower():
                        filtered_results.append(f"{timestamp} - {log_level}: {message}")

    except FileNotFoundError:
        return "Log file not found."

    return render_template('results.html', results=filtered_results[:10], total_results=len(filtered_results))

@app.route('/result/<int:index>')
def result(index):
    if index < 0 or index >= len(filtered_results):
        return "Invalid result index"
    
    result = filtered_results[index]
    return render_template('result_detail.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
