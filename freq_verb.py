import logging
import spacy
import os
from tqdm import tqdm
from collections import Counter

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def get_freq(nlp, file_path):
    text_file = open(file_path, 'r', encoding='utf-8')
    text_list = text_file.readlines()
    verb_list = []
    total_word = 0
    for line in tqdm(text_list):
        doc = nlp(line)
        verbs = [token.lemma_
                 for token in doc
                 if (not token.is_stop and
                     not token.is_punct and
                     token.pos_ == "VERB")]
        verb_list += verbs
        total_word += len(doc)
    total_verb = len(verb_list)
    verb_freq = Counter(verb_list)
    top_110 = verb_freq.most_common(110)
    text_file.close()
    return top_110, total_word, total_verb


def create_freq_data(input_folder, output_folder):
    # Uncomment to enable GPU acceleration
    # spacy.prefer_gpu()
    nlp = spacy.load("en_core_web_sm")
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        logging.info(f"Processing {file_path}...")
        top_list, total_word, total_verb = get_freq(nlp, file_path)
        out_path = os.path.join(output_folder, f"{file_name[:-4]}.tsv")
        with open(out_path, 'w', encoding='utf-8') as out_file:
            for line in top_list:
                line = [str(i) for i in line]
                line += [str(total_verb)]
                line += [str(total_word)]
                out_file.write("\t".join(line))
                out_file.write("\n")
        logging.info(f"File output in {out_path}")


def main():
    create_freq_data("input", "output")


if __name__ == "__main__":
    main()
