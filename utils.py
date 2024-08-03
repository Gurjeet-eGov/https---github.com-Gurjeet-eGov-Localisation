import re
import json

def formatCode(prefix, code):
    # returns sanitised text
    localised_code=re.sub(r'[^a-zA-Z0-9]', '_', code)
    prefix=re.sub(r'[^a-zA-Z0-9]', '_', prefix)
    localised_code=prefix+localised_code
    return localised_code.upper()


def get_json(path):
    """ 
    Takes JSON file from path and converts on Dict obj
    args: path(str)
    returns: Dictionary Obj
    dependancy: import json 
    """
    with open(path) as payload_file:
        return json.load(payload_file)


def extract_properties_keys(obj):
        keys_set = set()  # Use a set to track unique keys
        
        if isinstance(obj, dict):
            # If 'properties' key is found, process it
            if 'properties' in obj:
                # Add keys from this level of 'properties'
                keys_set.update(obj['properties'].keys())
                # Recursively check each nested 'properties'
                for key, value in obj['properties'].items():
                    if isinstance(value, dict):
                        # Recursively search nested properties
                        keys_set.update(extract_properties_keys(value))
                        
            # Recursively check for 'properties' in nested dictionaries
            for key, value in obj.items():
                if isinstance(value, dict):
                    keys_set.update(extract_properties_keys(value))

        return list(keys_set)  # Convert the set back to a list before returning