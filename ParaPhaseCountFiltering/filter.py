import argparse
import json

def filter_paraphrases(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:

        for line in infile:
            try:
                data = json.loads(line)
                for key, paraphrases in data.items():
                    # Check if the list has 3 or more paraphrases
                    if len(paraphrases) >= 3:
                        outfile.write(json.dumps({key: paraphrases}, ensure_ascii=False) + '\n')
            except json.JSONDecodeError:
                print(f"Skipping invalid line: {line}")

    print("Filtering complete.")

if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Filter paraphrases with fewer than 3 entries.')
    
    # Add arguments for input and output files
    parser.add_argument('--input_file', '-i', type=str, required=True, help='Path to the input JSONL file')
    parser.add_argument('--output_file', '-o', type=str, required=True, help='Path to the output JSONL file')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the filter function with the provided file paths
    filter_paraphrases(args.input_file, args.output_file)
