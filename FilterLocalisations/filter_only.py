import json
from collections import defaultdict

localisation_file = "localisations.json"
keyword = "mail"
search_field = "code"  # "message" or "code"


def read_messages_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def filter_exact_match(data, keyword, field):
    return [item for item in data if item.get(field, "") == keyword]


def filter_contains_case_insensitive(data, keyword, field):
    return [
        item for item in data
        if keyword.lower() in item.get(field, "").lower()
    ]


def filter_contains_case_sensitive(data, keyword, field):
    return [
        item for item in data
        if keyword in item.get(field, "")
    ]


def group_by_module(data):
    grouped = defaultdict(list)
    for item in data:
        grouped[item.get("module")].append(item)
    return dict(grouped)


def main():
    messages = read_messages_from_file(localisation_file)

    exact = group_by_module(filter_exact_match(messages, keyword, search_field))
    ci = group_by_module(filter_contains_case_insensitive(messages, keyword, search_field))
    cs = group_by_module(filter_contains_case_sensitive(messages, keyword, search_field))

    with open("grouped_exact_match.json", "w", encoding="utf-8") as f:
        json.dump(exact, f, indent=4, ensure_ascii=False)

    with open("grouped_case_insensitive.json", "w", encoding="utf-8") as f:
        json.dump(ci, f, indent=4, ensure_ascii=False)

    with open("grouped_case_sensitive.json", "w", encoding="utf-8") as f:
        json.dump(cs, f, indent=4, ensure_ascii=False)

    print("Filtering completed with original Unicode characters preserved.")


if __name__ == "__main__":
    main()
