import jsonlines

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

# Run the function to merge files
merge_sources_and_predictions(source_file_path, prediction_file_path, output_file_path)
