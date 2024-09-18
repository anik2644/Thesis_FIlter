import argparse
import json

# Define punctuation symbols
symbols = ''',;:?!'."-[]{}()–—―~'''

def remove_punctuation(text):
    """Remove specific punctuation from the text."""
    return ''.join(char for char in text if char not in symbols)

def process_paraphrases(input_file, output_file):
    """Process each line of the input file with punctuation filtering and write results to output file."""
    paraphrase_dict = {}

    # Read and process input file
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            try:
                data = json.loads(line.strip())
                for src, paraphrases in data.items():
                    src_filtered = remove_punctuation(src)
                    if src_filtered not in paraphrase_dict:
                        paraphrase_dict[src_filtered] = []
                    
                    for trg in paraphrases:
                        trg_filtered = remove_punctuation(trg)
                        paraphrase_dict[src_filtered].append(trg_filtered)
            
            except json.JSONDecodeError:
                print(f'Error decoding JSON for line: {line}')
                continue

    # Write the filtered results to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for src, paraphrases in paraphrase_dict.items():
            filtered_entry = {src: paraphrases}
            outfile.write(json.dumps(filtered_entry, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='Process input file with punctuation filtering')

    # Add the arguments
    parser.add_argument('--input_file', metavar='input_file', type=str, required=True, help='Path to the input JSONL file')
    parser.add_argument('--output_file', metavar='output_file', type=str, required=True, help='Path to the output JSONL file')

    args = parser.parse_args()

    input_file_path = args.input_file
    output_file_path = args.output_file

    process_paraphrases(input_file_path, output_file_path)

    print('Processing complete.')
