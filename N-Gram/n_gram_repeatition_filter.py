import argparse
import json
from bengali_stemmer.rafikamal2014 import RafiStemmer

def stem_string(string):
    stemmer = RafiStemmer()
    punc = '''।,;:?!'."-[]{}()–—―~'''
    for ele in string:
        if ele in punc:
            string = string.replace(ele, "")
    words = string.split()
    return ' '.join([stemmer.stem_word(word) for word in words])

def calculate_ngram_repeat(text, n_gram):
    """
    Returns the filtered sentences from the text which has n-gram repeats.

    Args:
        text (str) : string analyzed
        n_gram (int) : n_gram to consider during calculation of the repeat
    Returns:
        string with repeats (str) : string containing n-gram repeats
    """
    stemmed = stem_string(text)
    splitted = stemmed.split()
    
    # Generate all possible n-grams from the text
    n_grams = [' '.join(splitted[i:i+n_gram]) for i in range(len(splitted) - n_gram + 1)]
    
    # Count occurrences of each n-gram
    n_gram_counts = {}
    for ngram in n_grams:
        if ngram in n_gram_counts:
            n_gram_counts[ngram] += 1
        else:
            n_gram_counts[ngram] = 1
    
    # Collect n-grams that repeat
    repeated_ngrams = [ngram for ngram, count in n_gram_counts.items() if count > 1]
    
    if repeated_ngrams:
        return ' '.join(repeated_ngrams)
    
    return ''

def calculate_ngram_score(text, n_gram=2):
    if calculate_ngram_repeat(text, n_gram) != '':
        return 1  # Repetition found
    return 0  # No repetition

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='Path to the source and output file (JSONL format)')
    
    # Correct argument names
    parser.add_argument('--input_file', '-i', metavar='i', type=str, required=True, help='The path to the input file (JSONL format)')
    parser.add_argument('--output_file', '-o', metavar='o', type=str, required=True, help='The path to the output file (JSONL format)')

    args = parser.parse_args()

    input_path = args.input_file
    output_path = args.output_file

    print(f"Reading from: {input_path}")
    print(f"Saving output to: {output_path}")

    # Open the files and process them
    try:
        with open(input_path, 'r', encoding='utf-8') as input_file, \
                open(output_path, 'w', encoding='utf-8') as output_file:

            counter = 0
            # Process each line of the input JSONL file
            for line in input_file:
                line_obj = json.loads(line)
                sentence = list(line_obj.keys())[0]  # Extract the sentence
                predictions = line_obj[sentence]  # Extract the predictions

                print(f"Processing sentence: {sentence}")
                print(f"Predictions: {predictions}")

                # Check for n-gram repetitions in each prediction
                valid_predictions = []
                for pred in predictions:
                    score = calculate_ngram_score(pred, n_gram=2)
                    
                    # Print n-gram score for each prediction
                    print(f"Sentence: {pred} | N-Gram Score: {score}")
                    
                    if score == 0:
                        valid_predictions.append(pred)

                if valid_predictions:
                    # Write the output in the desired JSONL format
                    output_data = {sentence: valid_predictions}
                    output_file.write(json.dumps(output_data, ensure_ascii=False) + '\n')
                else:
                    counter += 1  # Count lines with only n-gram repeats

            print(f"Total lines with n-gram repetition filtered out: {counter}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
