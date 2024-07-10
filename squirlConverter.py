import os
import re
from datetime import datetime
import argparse

def parse_log_entry(entry):
    parts = entry.split()
    return {
        'ID': parts[0],
        'Timestamp': ' '.join(parts[1:4]),  # Combining date and time with 'UTC'
        'CallSign': parts[4],
        'Class': parts[5],
        'Section': parts[6]
    }

def read_log_file(file_path):
    log_entries = []
    with open(file_path, 'r') as file:
        for line in file:
            parsed_entry = parse_log_entry(line.strip())
            log_entries.append(parsed_entry)
    return log_entries

def extract_file_info(filename):
    pattern = r"^(.*)-(.*)-(.*)\.txt$"
    match = re.match(pattern, filename)
    if match:
        return match.groups()
    return None, None, None

def find_log_files(directory):
    log_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            call_sign, band, mode = extract_file_info(filename)
            if call_sign and band and mode:
                log_files.append({
                    'filename': filename,
                    'call_sign': call_sign,
                    'band': band,
                    'mode': mode
                })
    return log_files

def format_band(band):
    band_to_freq = {
        '160M': '1800',
        '80M': '3500',
        '40M': '7000',
        '20M': '14000',
        '15M': '21000',
        '10M': '28000'
    }
    return band_to_freq.get(band, band)

def format_mode(mode):
    if mode == 'SSB':
        return 'PH'
    elif mode == 'CW':
        return 'CW'
    elif mode == 'RTTY':
        return 'RY'
    else:
        return 'DG'

def format_date(timestamp):
    date_str = timestamp.split()[0]
    date_obj = datetime.strptime(date_str, "%m/%d/%y")
    return date_obj.strftime("%Y-%m-%d")

def format_time(timestamp):
    time_str = timestamp.split()[1]
    return time_str.replace(':', '')[:-2]

def parse_header_info():
    # Prompt user for header information
    header_info = {
        "START-OF-LOG": "3.0",
        "CONTEST": "ARRL-FD",
        "LOCATION": input("Enter your location (SECTION): "),
        "CALLSIGN": input("Enter your callsign: "),
        "CATEGORY": input("Enter the category (e.g., 6A): "),
        "CATEGORY-BAND": "ALL",
        "CATEGORY-MODE": "MIXED",
        "CATEGORY-OPERATOR": input("Enter the category operator (MULTI-OP/SINGLE-OP): "),
        "CATEGORY-POWER": input("Enter the category power (HIGH/LOW/QRP): "),
        "CATEGORY-STATION": input("Enter the category station (FIXED/MOBILE/PORTABLE): "),
        "CLAIMED-SCORE": input("Enter the claimed score: "),
        "CREATED-BY": "FD-SQUIRL2CAB",
        "NAME": input("Enter your name: "),
        "ADDRESS": input("Enter your address: "),
        "ADDRESS-CITY": input("Enter your city: "),
        "ADDRESS-STATE-PROVINCE": input("Enter your state or province: "),
        "ADDRESS-POSTALCODE": input("Enter your postal code: "),
        "ADDRESS-COUNTRY": input("Enter your country: "),
        "EMAIL": input("Enter your email: "),
        "OPERATORS": input("Enter the operators: "),
        "SOAPBOX": input("Enter the soapbox comment: ")
    }

    # Extract class and section from CATEGORY and LOCATION
    my_class = header_info.get('CATEGORY', '').split(' ', 1)[0]  # Extract class from CATEGORY
    my_section = header_info.get('LOCATION', '')  # Use LOCATION as the section

    return header_info, my_class, my_section

def create_output_file(log_files, my_class, my_section, output_path, header_info):
    with open(output_path, 'w') as output_file:
        # Write the header information
        for key, value in header_info.items():
            output_file.write(f"{key}: {value}\n")
        output_file.write("\n")
        
        for log_file in log_files:
            band_mhz = format_band(log_file['band'])
            mode = format_mode(log_file['mode'])
            for entry in log_file['entries']:
                date = format_date(entry['Timestamp'])
                time = format_time(entry['Timestamp'])
                line = f"QSO: {band_mhz} {mode} {date} {time} {log_file['call_sign']} {my_class} {my_section} {entry['CallSign']} {entry['Class']} {entry['Section']}"
                output_file.write(line + '\n')

        # Add the end of log line
        output_file.write("END-OF-LOG:\n")

# Define command-line arguments
parser = argparse.ArgumentParser(description='Convert log files to CAB format.')
parser.add_argument('output_file', nargs='?', default='output.cab', help='The target CAB file name.')

# Parse arguments
args = parser.parse_args()
output_path = args.output_file

# Ensure the output file has the .cab extension
if not output_path.lower().endswith('.cab'):
    output_path += '.cab'

# Get header information and class/section
header_info, my_class, my_section = parse_header_info()

# Example usage
directory = '.'  # Replace with the directory path where your log files are located
log_files = find_log_files(directory)

# Process each log file
for log_file in log_files:
    file_path = os.path.join(directory, log_file['filename'])
    log_entries = read_log_file(file_path)
    log_file['entries'] = log_entries

# Create the output file
create_output_file(log_files, my_class, my_section, output_path, header_info)

print(f"Output written to {output_path}")
