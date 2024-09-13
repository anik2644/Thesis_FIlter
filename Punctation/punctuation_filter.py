import argparse

# Define punctuation symbols
symbols = ''',;:?!'."-[]{}()–—―~'''

def remove_punctuation(text):
    """Remove specific punctuation from the text."""
    return ''.join(char for char in text if char not in symbols)

def process_lines(source_file, target_file, final_source, final_target):
    """Process each line of source and target files with punctuation filtering."""
    counter = 0

    for index, (src, trg) in enumerate(zip(source_file, target_file)):

        src = src.strip()
        trg = trg.strip()

        # Apply punctuation filter
        src_filtered = remove_punctuation(src)
        trg_filtered = remove_punctuation(trg)

        # Print original and filtered sentences
        print(f'Original Source: {src}')
        print(f'Filtered Source: {src_filtered}')
        print(f'Original Target: {trg}')
        print(f'Filtered Target: {trg_filtered}')
        print('---')

        if src[-1] == '"' and trg[-1] == '"':
            # Check if -2 pos has !?| or not
            if src[-2] in '?!।' and trg[-2] in '?!।':
                src_to_write, trg_to_write = '', ''
                if (src.count('"') % 2 == 0 and src.count('"') >= 2) and (trg.count('"') % 2 == 0 and trg.count('"') >= 2):
                    src_to_write = src_filtered
                    trg_to_write = trg_filtered
                elif src.count('"') == 1 and trg.count('"') == 1:
                    src_to_write = src_filtered[:-1]
                    trg_to_write = trg_filtered[:-1]
                if src_to_write and trg_to_write:
                    final_source.write(src_to_write + '\n')
                    final_target.write(trg_to_write + '\n')

        elif src[-1] == '\'' and trg[-1] == '\'':
            # Check if -2 pos has !?| or not
            if src[-2] in '?!।' and trg[-2] in '?!।':
                src_to_write, trg_to_write = '', ''
                if (src.count('\'') % 2 == 0 and src.count('\'') >= 2) and (trg.count('\'') % 2 == 0 and trg.count('\'') >= 2):
                    src_to_write = src_filtered
                    trg_to_write = trg_filtered
                elif src.count('\'') == 1 and trg.count('\'') == 1:
                    src_to_write = src_filtered[:-1]
                    trg_to_write = trg_filtered[:-1]
                if src_to_write and trg_to_write:
                    final_source.write(src_to_write + '\n')
                    final_target.write(trg_to_write + '\n')

        elif src[-1] == '"' and trg[-1] in '।!?':
            if src.count('"') == 1 and trg.count('"') == 0:
                if src[-2] in '?!।':
                    final_source.write(src_filtered[:-1] + '\n')
                    final_target.write(trg_filtered + '\n')

        elif src[-1] == '\'' and trg[-1] in '।!?':
            if src.count('\'') == 1 and trg.count('\'') == 0:
                if src[-2] in '?!।':
                    final_source.write(src_filtered[:-1] + '\n')
                    final_target.write(trg_filtered + '\n')

        elif trg[-1] == '"' and src[-1] in '।!?':
            if trg.count('"') == 1 and src.count('"') == 0:
                if trg[-2] in '?!।':
                    final_source.write(src_filtered + '\n')
                    final_target.write(trg_filtered[:-1] + '\n')

        elif trg[-1] == '\'' and src[-1] in '।!?':
            if trg.count('\'') == 1 and src.count('\'') == 0:
                if trg[-2] in '?!।':
                    final_source.write(src_filtered + '\n')
                    final_target.write(trg_filtered[:-1] + '\n')

        elif src[-1] in '।!?' and trg[-1] in '।!?':
            final_source.write(src_filtered + '\n')
            final_target.write(trg_filtered + '\n')

        if (index + 1) % 20000 == 0:
            print(f'Processed {index + 1} lines.')

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='Path to the source and target file')

    # Add the arguments
    parser.add_argument('--s', metavar='s', type=str, help='The path to the source file')
    parser.add_argument('--t', metavar='t', type=str, help='The path to the target file')

    args = parser.parse_args()

    source_path = args.s
    target_path = args.t

    with open(source_path, 'r', encoding='utf-8') as source_file, \
            open(target_path, 'r', encoding='utf-8') as target_file, \
            open('./source.bn', 'w', encoding='utf-8') as final_source, \
            open('./target.bn', 'w', encoding='utf-8') as final_target:
        
        process_lines(source_file, target_file, final_source, final_target)

    print('Processing complete.')
