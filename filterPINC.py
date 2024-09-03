import jsonlines
import json
import pandas as pd
import torch
from nltk import ngrams
import argparse
import os
import sys
from bengali_stemmer.rafikamal2014 import RafiStemmer


def merge_sources_and_predictions(source_path, prediction_path, output_path):
    # Open the source and prediction files
    with jsonlines.open(source_path) as source_file, \
         jsonlines.open(prediction_path) as prediction_file, \
         jsonlines.open(output_path, mode='w') as output_file:
        
        # Read the contents of both files into lists
        source_sentences = [line['sentence'] for line in source_file]
        prediction_sentences = [line['predictions'] for line in prediction_file]

        # Check if both files have the same number of lines
        if len(source_sentences) != len(prediction_sentences):
            print("The number of lines in source and prediction files do not match.")
            return
        
        # Merge and write the new structured data to the output file
        for source, predictions in zip(source_sentences, prediction_sentences):
            output_file.write({source: predictions})

# Specify the file paths
source_file_path = 'C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\source.jsonl'
prediction_file_path = 'C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\prediction.jsonl'
output_file_path = 'C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\filtersource.jsonl'


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

def calculate_pinc(key, value, N):
    pinc_scores = []
    key_tokens = key.split()
    value_tokens = value.split()

    for i in range(1, N+1):
        key_ngrams = list(ngrams(key_tokens, i))
        value_ngrams = list(ngrams(value_tokens, i))
        key_ngram_set = set(key_ngrams)
        value_ngram_set = set(value_ngrams)

        intersection = key_ngram_set.intersection(value_ngram_set)
        total_ngrams = len(value_ngram_set)

        if total_ngrams > 0:
            pinc_score = 1 - len(intersection) / total_ngrams
            pinc_scores.append(pinc_score)
        else:
            pinc_scores.append(1)  # Maximum dissimilarity if no n-grams

    return sum(pinc_scores) / len(pinc_scores)

def filter_dataset(jsonl_file, target_file, pinc_threshold):
    N = 4
    linecount = 0

    for line in jsonl_file.iter():
        linecount += 1
        hasfound = False
        trgts = {}

        for key, values in line.items():
            original_key = key
            key = stem_string(key)
            stemmed_values = [stem_string(value) for value in values]
            trgts[original_key] = []

            for value in stemmed_values:
                pinc_score = calculate_pinc(key, value, N)

                if pinc_score >= pinc_threshold:
                    hasfound = True
                    trgts[original_key].append(value)

        if hasfound:
            json.dump(trgts, target_file, ensure_ascii=False)
            target_file.write('\n')
            if linecount % 10000 == 0:
                print(linecount)

if __name__ == '__main__':


    merge_sources_and_predictions(source_file_path, prediction_file_path, output_file_path)


    # Create the parser
    parser = argparse.ArgumentParser(
        description='path to the input and output file and the pinc score threshold')

    # Add the arguments
    parser.add_argument('--l',
                        metavar='l',
                        type=str,
                        help='the path to the jsonl file with sources and corresponding paraphrases')

    parser.add_argument('--t',
                        metavar='t',
                        type=str,
                        help='the path to the generated target jsonl file')

    parser.add_argument('--p',
                        metavar='p',
                        type=float,
                        help='the desired pinc score threshold (0 - 1)')

    # Execute the parse_args() method
    args = parser.parse_args()

    jsonl_path = args.l
    target_path = args.t
    pinc_threshold = args.p

    target_file = open(target_path, 'w', encoding='utf-8')
    jsonl_file = jsonlines.open(jsonl_path)

    filter_dataset(jsonl_file, target_file, pinc_threshold)

    # closing all the files
    target_file.close()
    jsonl_file.close()