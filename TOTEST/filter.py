import jsonlines
import json
from nltk import ngrams
import argparse
import os
from bengali_stemmer.rafikamal2014 import RafiStemmer

def stem_string(string):
    """
    Returns a stemmed string without punctuations
    """
    stemmer = RafiStemmer()
    punc = '''।,;:?!'."-[]{}()–—―~'''
    string = ''.join([char for char in string if char not in punc])
    words = string.split()
    return ' '.join([stemmer.stem_word(word) for word in words])

def filter_dataset(jsonl_file, target_file, pinc_threshold):
    """
    Filters the jsonl file with the given PINC threshold and writes the filtered
    sentences to the target file
    """
    N = 4

    for obj in jsonl_file:
        predictions = obj.get("predictions", [])
        filtered_predictions = []

        for prediction in predictions:
            stemmed_prediction = stem_string(prediction)
            pinc_sum = 0
            prediction_n_grams = list(ngrams(stemmed_prediction.split(), N))

            for n_gram in prediction_n_grams:
                # This is a simplified PINC calculation placeholder
                pinc_sum += 0  # Normally you would compare with a reference here

            avg_pinc = pinc_sum / len(prediction_n_grams) if prediction_n_grams else 0

            if avg_pinc >= pinc_threshold:
                filtered_predictions.append(prediction)

        if filtered_predictions:
            json.dump({"predictions": filtered_predictions}, target_file, ensure_ascii=False)
            target_file.write("\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter JSONL based on PINC score threshold')
    parser.add_argument('--l', metavar='l', type=str, help='Path to the input JSONL file')
    parser.add_argument('--t', metavar='t', type=str, help='Path to the output JSONL file')
    parser.add_argument('--p', metavar='p', type=float, help='PINC score threshold (0 - 1)')
    args = parser.parse_args()

    with jsonlines.open(args.l) as jsonl_file, open(args.t, 'w', encoding='utf-8') as target_file:
        filter_dataset(jsonl_file, target_file, args.p)
