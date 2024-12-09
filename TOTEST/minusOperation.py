import json

file1_path = r"C:\Users\anik1\Documents\Thesis\bengali-stemmer-dev\bengali-stemmer-dev\filtersource.jsonl"
file2_path = r"C:\Users\anik1\Documents\Thesis\bengali-stemmer-dev\bengali-stemmer-dev\BertSCORE\filtered_paraphrases.jsonl"
output_file_path = "minus.jsonl"

# Read the first file into a dictionary
file1_data = {}
with open(file1_path, 'r', encoding='utf-8') as f1:
    for line in f1:
        entry = json.loads(line.strip())
        file1_data.update(entry)

# Read the second file into a dictionary
file2_data = {}
with open(file2_path, 'r', encoding='utf-8') as f2:
    for line in f2:
        entry = json.loads(line.strip())
        file2_data.update(entry)

# Find entries that are in file1 but not in file2
difference = {}
for key, value in file1_data.items():
    if key in file2_data:
        # If key is in both files, filter out paraphrases that are already in file2
        new_paraphrases = [p for p in value if p not in file2_data[key]]
        if new_paraphrases:
            difference[key] = new_paraphrases
    else:
        # If key is only in file1, take the entire paraphrase list
        difference[key] = value

# Write the differences to a new JSONL file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for key, value in difference.items():
        json_record = json.dumps({key: value}, ensure_ascii=False)
        output_file.write(json_record + "\n")

print(f"Difference data has been written to {output_file_path}")