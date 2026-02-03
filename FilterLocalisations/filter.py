import json
import requests
from collections import defaultdict

# Define URL and file paths
url = "http://localhost:8082/localization/messages/v1/_search?locale=en_IN&tenantId=pg"
localisation_file = "localisations.json"
keyword = "(Top 3 performing Localities)"

# Function to fetch localization messages
def fetchMessages():
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "RequestInfo": {
            "apiId": "Rainmaker",
            "ver": ".01",
            "ts": "",
            "action": "_create",
            "did": "1",
            "key": "",
            "msgId": "20170310130900|en_IN",
            "authToken": "a4c35063-6a87-4671-a63b-8b92de760a4f"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Check for HTTP errors
        messages = response.json().get("messages", [])
        
        # Write fetched messages to localisation file
        with open(localisation_file, "w") as output_file:
            json.dump(messages, output_file, indent=4)
        
        print("Fetched messages written to localisations.json")
        return messages

    except requests.exceptions.RequestException as e:
        print(f"Error fetching messages: {e}")
        return []

# Read messages from local file (if needed)
def read_messages_from_file(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

# Filtering functions for different criteria
def filter_exact_match(data, keyword):
    """Return items where the message exactly matches the keyword."""
    return [item for item in data if item["message"] == keyword]

def filter_contains_case_insensitive(data, keyword):
    """Return items where the message contains the keyword, case insensitive."""
    return [item for item in data if keyword.lower() in item["message"].lower()]

def filter_contains_case_sensitive(data, keyword):
    """Return items where the message contains the keyword, case sensitive."""
    return [item for item in data if keyword in item["message"]]

# Group results by module for easier organization
def group_by_module(data):
    grouped_data = defaultdict(list)
    for item in data:
        grouped_data[item["module"]].append(item)
    return dict(grouped_data)  # Convert to regular dict for JSON compatibility

# Main execution flow
def main():
    # Fetch messages from API and save them to file
    messages = fetchMessages()

    # If no messages were fetched, try reading from local file
    if not messages:
        messages = read_messages_from_file(localisation_file)

    # Perform different types of filtering
    exact_match_results = filter_exact_match(messages, keyword)
    case_insensitive_results = filter_contains_case_insensitive(messages, keyword)
    case_sensitive_results = filter_contains_case_sensitive(messages, keyword)

    # Group each set of results by module
    grouped_exact_match = group_by_module(exact_match_results)
    grouped_case_insensitive = group_by_module(case_insensitive_results)
    grouped_case_sensitive = group_by_module(case_sensitive_results)

    # Save grouped results to separate JSON files for each filter type
    with open("grouped_exact_match.json", "w") as output_file:
        json.dump(grouped_exact_match, output_file, indent=4)
    
    with open("grouped_case_insensitive.json", "w") as output_file:
        json.dump(grouped_case_insensitive, output_file, indent=4)

    with open("grouped_case_sensitive.json", "w") as output_file:
        json.dump(grouped_case_sensitive, output_file, indent=4)

    print("Grouped results saved to JSON files for each filter type.")

# Run the script
if __name__ == "__main__":
    main()
