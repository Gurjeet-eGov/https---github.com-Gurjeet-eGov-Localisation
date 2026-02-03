import pandas as pd

# Replace with your Google Sheets pubhtml link
url = "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vTu4YXmvNIq_iOk3nIY94GRWE-lzYH-x2tr8YQk5bYgYDF6KG9JDYD6_xNXpQqKd5bnUdoLw9TDIqfs/pubhtml"

# Read tables from the HTML page
tables = pd.read_html(url)

# Save all sheets (tables) into an Excel file
output_file = "google_sheets.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for i, table in enumerate(tables):
        sheet_name = f"Sheet_{i+1}"  # Rename based on sheet index
        table.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Excel file saved as '{output_file}'")
