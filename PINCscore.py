import jsonlines
import argparse
from nltk import ngrams
from bengali_stemmer.rafikamal2014 import RafiStemmer

def stem_string(string):
    """
    Returns a stemmed string without punctuations.

    Args:
        string (str): String to be stemmed.

    Returns:
        str: Stemmed version of the string.
    """
    stemmer = RafiStemmer()
    punc = '''।,;:?!'."-[]{}()–—―~'''
    string = ''.join(char for char in string if char not in punc)
    words = string.split()
    return ' '.join(stemmer.stem_word(word) for word in words)

def calculateScore(sourcefile, predictionfile):
    """
    Calculates and prints PINC score for multiple predictions per source sentence.

    Args:
        sourcefile (jsonlines.Reader): The source file.
        predictionfile (jsonlines.Reader): The prediction file.
    """
    N = 4

    for source_line, pred_line in zip(sourcefile, predictionfile):
        source = stem_string(source_line['sentence'])
        print("Source Sentence:", source)
        predictions = pred_line['predictions']
        for idx, prediction in enumerate(predictions, start=1):
            prediction = stem_string(prediction)
            pinc_sum = 0
            for i in range(N):
                key_n_grams = list(ngrams(source.split(), i + 1))
                value_n_grams = list(ngrams(prediction.split(), i + 1))
                overlap_count = sum(1 for key in key_n_grams if key in value_n_grams)
                
                # Calculate PINC for this n-gram size
                if value_n_grams:
                    pinc_sum += (1 - overlap_count / len(value_n_grams))
                
            # Print PINC score for this prediction
            score = pinc_sum / N
            print(f"Score for prediction {idx}: {score}")
        print()  # Print a blank line after each set of predictions

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Path to source and prediction JSONL files')
    parser.add_argument('--s', metavar='s', type=str, help='the path to the source JSONL file')
    parser.add_argument('--p', metavar='p', type=str, help='the path to the prediction JSONL file')
    args = parser.parse_args()

    # Open files and calculate score
    with jsonlines.open(args.s, mode='r') as sourcefile, jsonlines.open(args.p, mode='r') as predictionfile:
        calculateScore(sourcefile, predictionfile)
    # closing all the files
    sourcefile.close()
    predictionfile.close()