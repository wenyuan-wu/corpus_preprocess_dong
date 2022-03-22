import os
from tqdm import tqdm
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def total_word_count(input_folder):
    process_bar = tqdm(os.listdir(input_folder))
    words_list = []
    for file_name in process_bar:

        file_path = os.path.join(input_folder, file_name)
        words = file_word_count(file_path)
        process_bar.set_description("Processing {}, words: {}".format(file_name, words))
        words_list.append(words)
    total = sum(words_list)
    print(f"total words in {input_folder}: {total}")


def file_word_count(file_path):
    with open(file_path, 'r', encoding='utf-8') as infile:
        sents = infile.read()
        lines = sents.split()
        words = len(lines)
    return words


def main():
    # adjust the following variable values to get the desired output
    input_folder = "output_data"
    total_word_count(input_folder)


if __name__ == '__main__':
    main()
