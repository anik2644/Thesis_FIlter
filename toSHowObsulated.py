import json

# Load the source and output jsonl files into lists of dictionaries
def load_jsonl(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]

# Write a list of dictionaries to a jsonl file
def write_jsonl(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for entry in data:
            file.write(json.dumps(entry, ensure_ascii=False) + '\n')

# Find the differences between source and output files
def find_obsoleted_sentences(source_file, output_file, output_diff_file):
    # Load data
    source_data = load_jsonl(source_file)
    output_data = load_jsonl(output_file)
    
    # Convert output data to a dictionary for easier lookup
    output_dict = {list(item.keys())[0]: list(item.values())[0] for item in output_data}
    
    # List to store sentences that have been removed
    obsoleted_sentences = []
    
    # Compare source data with output data
    for source_entry in source_data:
        source_key = list(source_entry.keys())[0]
        source_sentences = set(source_entry[source_key])
        
        # If key exists in output, compare the sentences
        if source_key in output_dict:
            output_sentences = set(output_dict[source_key])
            # Find sentences that are in source but not in output
            removed_sentences = source_sentences - output_sentences
            
            # If there are removed sentences, add them to the result
            if removed_sentences:
                obsoleted_sentences.append({source_key: list(removed_sentences)})
        else:
            # If the key doesn't exist in output, all sentences are removed
            obsoleted_sentences.append({source_key: list(source_sentences)})
    
    # Write obsoleted sentences to new jsonl file
    write_jsonl(output_diff_file, obsoleted_sentences)

# Specify file names
source_file = "C:\\Users\\anik\\Desktop\\bengali-stemmer-dev\\filtersource.jsonl"
output_file = "C:\\Users\\anik\\Desktop\\bengali-stemmer-dev\\finaloutput.jsonl"
output_diff_file = 'C:\\Users\\anik\\Desktop\\bengali-stemmer-dev\\obsoleted_sentences.jsonl'


# Run the function
find_obsoleted_sentences(source_file, output_file, output_diff_file)
