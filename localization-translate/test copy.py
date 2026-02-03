import json
from googletrans import Translator

# Input and output file paths
input_file = "rainmaker-pgr.json"          # your original file
output_file = "hindi/rainmaker-pgr.json"   # translated file

def translate_messages(input_file, output_file):
    # Load JSON data
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    translator = Translator()
    total = len(data)

    for i, item in enumerate(data, start=1):
        if "message" in item and item["message"].strip():
            try:
                translated = translator.translate(item["message"], src="en", dest="hi")
                item["message"] = translated.text
            except Exception as e:
                print(f"⚠️ Failed to translate: {item['message']} -> {e}")

        # Show progress
        print(f"[{i}/{total}] Translated", end="\r")

    # Save translated JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"\n✅ Translation completed. File saved as {output_file}")

if __name__ == "__main__":
    translate_messages(input_file, output_file)
