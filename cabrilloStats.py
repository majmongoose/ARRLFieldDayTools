import re
import pandas as pd
import argparse

# Define the frequency to band conversion
frequency_to_band = {
    '1800': '160m',
    '3500': '80m',
    '7000': '40m',
    '14000': '20m',
    '21000': '15m',
    '28000': '10m',
}

# Define a function to parse the QSO lines
def parse_qso_line(line):
    # Use regex to match the QSO line and extract the mode and frequency
    match = re.match(r"QSO:\s+(\d+)\s+(\w+)\s+\d{4}-\d{2}-\d{2}\s+\d{4}\s+\w+\s+\w+\s+\w+\s+\w+", line)
    if match:
        frequency, mode = match.groups()
        band = frequency_to_band.get(frequency, None)  # Convert frequency to band
        if band:
            return mode, band
    return None, None

# Define a function to read the log file and count QSOs
def read_log_file(file_path):
    # Initialize counters for QSOs
    counts = {'CW': {}, 'PH': {}, 'RY': {}, 'DG': {}}
    
    # Read the log file
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('QSO:'):
                mode, band = parse_qso_line(line.strip())
                if mode and mode in counts:
                    if band not in counts[mode]:
                        counts[mode][band] = 0
                    counts[mode][band] += 1
    
    # Convert counts to a DataFrame for better display
    # Define all possible bands
    all_bands = ['160m', '80m', '40m', '20m', '15m', '10m']
    
    # Initialize the DataFrame with all bands and modes
    data = {band: {mode: counts[mode].get(band, 0) for mode in ['CW', 'DG', 'PH', 'RY']} for band in all_bands}
    df = pd.DataFrame(data).T.fillna(0).astype(int)
    
    return df

# Define a function to print the results
def print_summary(df):
    print("QSO Counts by Band and Mode:")
    print(df)

# Main function to run the script
def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Process a log file to count QSOs by band and mode.")
    parser.add_argument('file_path', help="Path to the log file")
    args = parser.parse_args()
    
    # Read the log file and get QSO counts
    df = read_log_file(args.file_path)
    
    # Print the summary
    print_summary(df)

if __name__ == "__main__":
    main()
