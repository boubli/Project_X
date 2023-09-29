from flask import Flask, render_template, request, send_file
import os
import logging
import io
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Configure logging
log_format = "%(asctime)s [%(levelname)s] - %(message)s"
log_file = "app.log"

logging.basicConfig(filename=log_file, level=logging.DEBUG, format=log_format)

# Define routes and functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
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
        logging.error("No log file uploaded.")
        return "No log file uploaded."

    # Initialize a list to store filtered log entries
    filtered_results = []

    try:
        if log_file_path.endswith('.json'):
            # Handle JSON log file
            with open(log_file_path, 'r') as json_file:
                log_entries = json.load(json_file)
        elif log_file_path.endswith('.xml'):
            # Handle XML log file
            tree = ET.parse(log_file_path)
            root = tree.getroot()
            log_entries = []
            for entry in root:
                log_entry = {
                    'timestamp': entry.find('timestamp').text,
                    'logLevel': entry.find('logLevel').text,
                    'message': entry.find('message').text,
                    'errorCode': entry.find('errorCode').text
                }
                log_entries.append(log_entry)
        else:
            logging.error("Unsupported log file format.")
            return "Unsupported log file format."

        # Process log entries based on the search criteria
        for log_entry in log_entries:
            # Check if the timestamp falls within the date range
            # You may need to convert timestamp to a datetime object and compare here
            # Example: timestamp = datetime.strptime(log_entry['timestamp'], '%Y-%m-%d %H:%M:%S')
            # Filter by start_date and end_date

            # Check if the keyword exists in the log message
            if keyword.lower() in log_entry['message'].lower():
                filtered_results.append(f"{log_entry['timestamp']} - {log_entry['logLevel']}: {log_entry['message']}")

    except FileNotFoundError:
        logging.error("Log file not found.")
        return "Log file not found."
    except Exception as e:
        logging.error(f"Error processing log file: {str(e)}")
        return f"Error processing log file: {str(e)}"

    # Log the search parameters and results
    logging.info(f"Search Parameters - Start Date: {start_date}, End Date: {end_date}, Keyword: {keyword}")
    logging.info(f"Filtered Results: {filtered_results}")

    return render_template('results.html', results=filtered_results)

@app.route('/download_results')
def download_results():
    # Retrieve filtered results from the query parameter
    filtered_results = request.args.getlist('filtered_results')

    # Create a temporary in-memory text file
    output = io.StringIO()
    output.write('\n'.join(filtered_results))

    # Return the in-memory file as a downloadable text file
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='filtered_results.txt', mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
