import json
import xml.etree.ElementTree as ET

# Function to convert .log to JSON format
def log_to_json(input_file, output_file):
    log_entries = []
    with open(input_file, 'r') as log_file:
        for line in log_file:
            line = line.strip()
            if line.startswith("[") and "] " in line:
                timestamp, message = line.split("] ", 1)
                log_entry = {
                    "timestamp": timestamp[1:],
                    "message": message
                }
                log_entries.append(log_entry)
    
    with open(output_file, 'w') as json_file:
        json.dump(log_entries, json_file, indent=4)

# Function to convert XML logs to .log format
def xml_to_log(input_file, output_file):
    with open(input_file, 'r') as xml_file, open(output_file, 'w') as log_file:
        log_file.write("XML Logs converted to .log format:\n")
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for log_entry in root.findall(".//logEntry"):
            timestamp = log_entry.find("timestamp").text
            message = log_entry.find("message").text
            log_file.write(f"[{timestamp}] {message}\n")

# Example usage
input_log_file = "sample.log"  # Replace with your .log input file
output_json_file = "output.json"  # Replace with the desired output .json file

input_xml_file = "input.xml"  # Replace with your XML input file
output_xml_log_file = "output_xml.log"  # Replace with the desired output .log file

log_to_json(input_log_file, output_json_file)
xml_to_log(input_xml_file, output_xml_log_file)
