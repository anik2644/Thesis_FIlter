import jsonlines

# File path (update with your actual file path)
file_path = r"C:\Users\anik1\Desktop\bengali-stemmer-dev\filtersource.jsonl"

# List to store results
results = []

try:
    # Open and read the JSONL file
    with jsonlines.open(file_path) as reader:  # Open the JSONL file
        for index, obj in enumerate(reader):  # Iterate over each line in the file
            for sentences in obj.values():  # Access the list of sentences
                for sentence in sentences:  # Iterate over sentences in the list
                    if sentence.startswith(
                        "১০"
                    ):  # Check if the sentence starts with "১৬"
                        results.append((index, sentence))

    # Print results
    print("Sentences starting with '১৬' and their indexes:")
    for result in results:
        print(f"Index: {result[0]}, Sentence: {result[1]}")

    # Save results to a text file
    output_file = "sentences_starting_with_১৬.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for result in results:
            f.write(f"Index: {result[0]}, Sentence: {result[1]}\n")

    print(f"\nResults saved to {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")
