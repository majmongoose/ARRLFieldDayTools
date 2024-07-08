import re
from datetime import datetime
import argparse

def parse_adi_line(line):
    pattern = r'<([^:]+):(\d+)>([^<]*)'
    matches = re.findall(pattern, line)
    return {field: value for field, _, value in matches}

def convert_to_new_format(parsed_data, class_, section):
    # Extract required fields with default values if not present
    band_freq = parsed_data.get('band', '')
    mode = parsed_data.get('mode', '')
    qso_date = parsed_data.get('qso_date', '')
    time_on = parsed_data.get('time_on', '')
    operator = parsed_data.get('operator', '')
    call = parsed_data.get('call', '')
    comment = parsed_data.get('comment', '').replace('-', ' ')

    # Convert mode to PH if it's SSB
    if mode == 'SSB':
        mode = 'PH'

    # Extract CLASS and SECTION from comment
    comment_parts = comment.split(' ', 1)
    log_class = comment_parts[0] if len(comment_parts) > 0 else ''
    log_section = comment_parts[1] if len(comment_parts) > 1 else ''

    # Convert band to frequency
    band_to_freq = {
        '160M': '1800',
        '80M': '3500',
        '40M': '7000',
        '20M': '14000',
        '15M': '21000',
        '10M': '28000',
    }
    frequency = band_to_freq.get(band_freq, band_freq)

    # Reformat date from YYYYMMDD to YYYY-MM-DD if qso_date is present
    formatted_date = ''
    if qso_date:
        formatted_date = datetime.strptime(qso_date, '%Y%m%d').strftime('%Y-%m-%d')

    # Generate the output line and remove extra spaces
    output_line = f"QSO: {frequency} {mode} {formatted_date} {time_on} {operator} {class_} {section} {call} {log_class} {log_section}"
    return ' '.join(output_line.split())

def convert_file(source_file, target_file, header_info):
    class_ = header_info.get('CATEGORY', '').split(' ', 1)[0]  # Extract class from CATEGORY
    section = header_info.get('LOCATION', '')  # Use LOCATION as the section

    with open(source_file, 'r') as src, open(target_file, 'w') as tgt:
        # Write the header information
        for key, value in header_info.items():
            tgt.write(f"{key}: {value}\n")
        tgt.write("\n")

        for line in src:
            line = line.strip()
            if line and line.startswith('<'):  # Skip empty lines and lines not starting with '<'
                parsed_data = parse_adi_line(line)
                converted_line = convert_to_new_format(parsed_data, class_, section)
                tgt.write(converted_line + '\n')

        # Add the end of log line
        tgt.write("END-OF-LOG:\n")

# Define command-line arguments
parser = argparse.ArgumentParser(description='Convert ADIF log file to CAB format.')
parser.add_argument('source_file', nargs='?', default=None, help='The source ADIF file name.')
parser.add_argument('target_file', nargs='?', default=None, help='The target CAB file name.')

# Parse arguments
args = parser.parse_args()

# Prompt the user for the source and target file names if not provided via command-line
if args.source_file is None:
    source_file = input("Enter the source file name: ")
else:
    source_file = args.source_file

if args.target_file is None:
    target_file = input("Enter the target file name: ")
else:
    target_file = args.target_file

# Prompt the user for the header information
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
    "CREATED-BY": "FD-Adif2Cab",
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

convert_file(source_file, target_file, header_info)
