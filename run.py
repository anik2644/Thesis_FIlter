import subprocess

def run_command(command):
    """Run a command and check for errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Output:\n{result.stdout}")
        print(f"Error:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"Output:\n{e.stdout}")
        print(f"Error:\n{e.stderr}")

if __name__ == '__main__':
    commands = [
        'python PincFilter/filterPINC.py --l "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\filtersource.jsonl" --t "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\PincFilter\\filteredoutput.jsonl" --p 0.9',
        'python BertSCORE\\bert_score\\testBertScore.py --s "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\PincFilter\\filteredoutput.jsonl" --o "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\BertSCORE\\bert_score\\testBertOutput.jsonl"',
        'python BertSCORE\\bert_score\\filterBanglaBert.py --j "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\BertSCORE\\bert_score\\testBertOutput.jsonl" --o "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\BertSCORE\\filtered_paraphrases.jsonl" --l 0.80 --u 0.90',
        'python N-Gram\\n_gram_repeatition_filter.py --input_file "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\BertSCORE\\filtered_paraphrases.jsonl" --output_file "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\N-Gram\\NGram_filteredOutput.jsonl"',
        'python Punctation\\punctuation_filter.py --input_file "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\N-Gram\\NGram_filteredOutput.jsonl" --output_file "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\Punctation\\punctuationFilterOutput.jsonl"',
        'python ParaPhaseCountFiltering\\filter.py --input_file "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\Punctation\\punctuationFilterOutput.jsonl" --output_file "C:\\Users\\anik1\\Documents\\Thesis\\bengali-stemmer-dev\\bengali-stemmer-dev\\finaloutput.jsonl"'
    ]

    for command in commands:
        run_command(command)
