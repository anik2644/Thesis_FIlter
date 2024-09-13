import argparse
import json
from bengali_stemmer.rafikamal2014 import RafiStemmer

"""Must be kept inside the rafikamal stemmer"""

def stem_string(string):
    """
    returns a stemmed string without punctuations

    Args:
        string (str) : string to be stemmed
    Returns:
        stemmed_string (str) : stemmed version of the string
    """
    stemmer = RafiStemmer()
    punc = '''।,;:?!'."-[]{}()–—―~'''

    for ele in string:
        if ele in punc:
            string = string.replace(ele, "")
    words = string.split()
    return ' '.join([stemmer.stem_word(word) for word in words])


def calculate_ngram_repeat(text, n_gram):
    """
    returns the filtered sentences from the text which has n gram-repeats

    Args:
        text (str) : string analyzed
        n_gram (str) : n_gram to consider during calculation of the repeat
    Returns:
        string with repeats (str) : string containing n-gram repeats
    """
    stemmed = stem_string(text)
    splitted = stemmed.split()

    for i, baseword in enumerate(splitted):
        for j, cmpword in enumerate(splitted[i+1:]):
            if baseword == cmpword:
                if len(splitted) - i - j - 1 > j:
                    trackflag = True
                    for k in range(1, j+1):
                        if splitted[i+k] != splitted[i+1+j+k]:
                            trackflag = False
                            break
                    if trackflag:
                        if j+1 >= n_gram:
                            return ' '.join([s for s in splitted[i:i+j+1]])
    return ''


def calculate_ngram_score(text, n_gram=2):
    """
    returns a binary score for a sentence based on n-gram repetition.
    1 if n-gram repetition is found, 0 otherwise.

    Args:
        text (str): The sentence or prediction to evaluate
        n_gram (int): N-gram size to look for (default is 2)
    
    Returns:
        int: 1 if there's n-gram repetition, 0 otherwise.
    """
    if calculate_ngram_repeat(text, n_gram) != '':
        return 1  # Repetition found
    return 0  # No repetition


if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='path to the source and target file')

    # Add the arguments
    parser.add_argument('--s', metavar='s', type=str, help='the path to the source file')
    parser.add_argument('--t', metavar='t', type=str, help='the path to the target file')

    args = parser.parse_args()

    source_path = args.s
    target_path = args.t

    with open(source_path, 'r', encoding='utf-8') as source_file, \
            open(target_path, 'r', encoding='utf-8') as target_file, \
            open('ngram_filtered_source.bn', 'w', encoding='utf-8') as final_source, \
            open('ngram_filtered_target.bn', 'w', encoding='utf-8') as final_target:

        counter = 0

        # Process each source and prediction line
        for source_line, target_line in zip(source_file, target_file):
            source_obj = json.loads(source_line)
            target_obj = json.loads(target_line)

            sentence = source_obj['sentence']
            predictions = target_obj['predictions']

            # Check for n-gram repetitions in each prediction
            valid_predictions = []
            for pred in predictions:
                score = calculate_ngram_score(pred, n_gram=2)
                print(f"Sentence: {pred} | N-Gram Score: {score}")
                
                # If the prediction has no n-gram repeats (score == 0), it's valid
                if score == 0:
                    valid_predictions.append(pred)

            if valid_predictions:
                # If there are valid predictions without n-gram repeats, write to final files
                final_source.write(json.dumps(source_obj, ensure_ascii=False) + '\n')
                final_target.write(json.dumps(target_obj, ensure_ascii=False) + '\n')
            else:
                counter += 1  # Count how many lines had n-gram repeats

            if (counter + 1) % 20000 == 0:
                print(f'Processed {counter + 1} lines with n-gram repeats.')

    print(f"Total lines with n-gram repetition filtered out: {counter}")
