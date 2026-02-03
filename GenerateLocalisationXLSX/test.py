import json
import csv

"""get list of unique localization codes (only codes list)"""
# Read JSON file
with open("localisations.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract unique codes
unique_codes = {item["code"] for item in data}

# Write to CSV file
with open("unique_codes.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Code"])  # Write header
    for code in sorted(unique_codes):  # Sorting for consistency
        writer.writerow([code])

print("CSV file 'unique_codes.csv' has been created successfully.")
