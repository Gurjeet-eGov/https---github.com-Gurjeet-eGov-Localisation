import json
import pandas as pd
from pathlib import Path

# Load the JSON data
input_file = "localisations.json"
output_file = "localisations (PROD, SMS, pn_IN).xlsx"

# Read the input JSON file
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Organize data by module codes
module_data = {}
for item in data:
    module_code = item["module"]
    if module_code not in module_data:
        module_data[module_code] = []
    module_data[module_code].append(item)

# Create an Excel writer
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    for module_code, records in module_data.items():
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(records)
        # Write the DataFrame to a sheet named after the module code
        df.to_excel(writer, sheet_name=module_code, index=False)

print(f"Excel file '{output_file}' created successfully!")
