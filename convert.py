import dicttoxml
import json
import logging

# Configure logging to save to a log file
logging.basicConfig(filename='conversion.log', level=logging.INFO, format='%(asctime)s - %(message)s')

try:
    # Specify the path to your JSON file
    json_file_path = 'path/to/your/json_file.json'

    # Load JSON data from the file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Convert JSON to XML
    xml_data = dicttoxml.dicttoxml(json_data)

    # Log the XML data
    logging.info("Converted JSON to XML:\n%s", xml_data)

    # You can optionally print the XML data
    print("XML Data:")
    print(xml_data)

    # Save the XML data to a log file
    with open("output.xml", "wb") as xml_file:
        xml_file.write(xml_data)

    print("XML data saved to 'output.xml'")
except Exception as e:
    # Handle any exceptions and log them
    logging.error("Error occurred: %s", str(e))
    print("Error:", str(e))
