import json

# Input and output file paths
input_file_path = r"C:\Users\anik\Desktop\bengali-stemmer-dev\finaloutput.jsonl"
output_file_path = r"C:\Users\anik\Desktop\bengali-stemmer-dev\readyforHF.jsonl"

# Initialize an empty list to store the results
results = []

# Read from the input file and process the data
with open(input_file_path, "r", encoding="utf-8") as infile:
    for line in infile:
        json_obj = json.loads(line.strip())
        for source, paraphrases in json_obj.items():
            for paraphrase in paraphrases:
                results.append({"source": source, "paraphrase": paraphrase})

# Write the results to the output JSONL file
with open(output_file_path, "w", encoding="utf-8") as outfile:
    for entry in results:
        outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"Processed data has been saved to {output_file_path}")











# import json

# # Input JSON data as a string
# data = '''
# {"কীভাবে আমি ভালো শিক্ষার্থী হতে পারি?": ["ভালো শিক্ষার্থী হওয়ার উপায় কী?", "ভালো ছাত্র হতে গেলে কী করতে হবে?", "ভালো শিক্ষার্থী হওয়ার জন্য কি কি পদক্ষেপ প্রয়োজন?", "ভালো শিক্ষার্থী হওয়ার সহজ উপায় কী?"]}
# {"তুমি আজকের পরীক্ষায় কেমন করেছো?": ["আজকের পরীক্ষাটি কেমন হলো?", "তোমার পরীক্ষা কেমন গেছে?", "তুমি কি আজকের পরীক্ষায় ভালো করেছো?", "পরীক্ষায় তোমার পারফরম্যান্স কেমন?", "আজকের পরীক্ষার ফল কেমন হয়েছে?"]}
# {"অনুগ্রহ করে দরজা বন্ধ করো।": ["দয়া করে দরজাটি লাগাও!", "দরজা বন্ধ করা যাবে?", "দরজাটি বন্ধ করার অনুরোধ করছি।"]}
# {"আজকের আবহাওয়া খুব সুন্দর!": ["আজকের আবহাওয়া একদম মনমতো!", "আজকের দিনটি কত সুন্দর!", "আজকের আবহাওয়ায় ঘুরতে যাওয়া উচিত!", "আজকের আবহাওয়াটা দারুণ!"]}
# {"তুমি কবে থেকে নতুন চাকরিতে যোগ দিচ্ছো?": ["তোমার নতুন চাকরির শুরু কবে?", "তুমি কি নতুন চাকরিতে যোগ দিয়েছ?", "কবে থেকে তুমি নতুন চাকরিতে কাজ শুরু করবে?", "নতুন চাকরিতে যাওয়ার তারিখ কি ঠিক হয়েছে?", "তুমি কি জানো কবে নতুন চাকরিতে যোগ দিচ্ছ?"]}
# '''

# # Load each JSON object and extract source-paraphrase pairs
# results = []
# for line in data.strip().splitlines():
#     json_obj = json.loads(line)
#     for source, paraphrases in json_obj.items():
#         for paraphrase in paraphrases:
#             results.append((source, paraphrase))

# # Print the resulting tuples
# for result in results:
#     print(result)
