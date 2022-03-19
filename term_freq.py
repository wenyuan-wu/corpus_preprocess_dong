import os
from tqdm import tqdm
import pandas as pd
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def get_keywords_list(keyword_folder, keyword_file):
    file_path = os.path.join(keyword_folder, keyword_file)
    keyword_list = []
    with open(file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.rstrip('\n')
            keyword_list.append(line)
    return keyword_list


def get_freq_data_list(input_folder):
    process_bar = tqdm(os.listdir(input_folder))
    df_list = []
    for file_name in process_bar:
        process_bar.set_description("Processing {}".format(file_name))
        file_path = os.path.join(input_folder, file_name)
        df = pd.read_excel(file_path, skiprows=4)
        df_list.append(df)
    return df_list


def search_item_in_df(keyword, df):
    result_df = df.loc[df['Item'].str.contains(keyword, case=False)]
    return result_df


def creat_term_freq_df(keyword_list, df_list, input_folder, output_folder):
    file_names = os.listdir(input_folder)
    process_bar = tqdm(enumerate(df_list))
    for idx, df in process_bar:
        process_bar.set_description("Processing {}".format(file_names[idx]))
        result_list = []
        for item in keyword_list:
            result_df = search_item_in_df(item, df)
            result_list.append(result_df)
        freq_df = pd.concat(result_list)
        outfile_path = os.path.join(output_folder, file_names[idx])
        freq_df.to_excel(outfile_path)


def main():
    # adjust the following variable values to get the desired output
    # keywords should not start with kapital
    keyword_folder = "term_data"
    keyword_file = "keyword.txt"
    output_folder = "term_freq_data"
    input_folder = "freq_data"

    keyword_list = get_keywords_list(keyword_folder, keyword_file)
    df_list = get_freq_data_list(input_folder)
    creat_term_freq_df(keyword_list, df_list, input_folder, output_folder)


if __name__ == '__main__':
    main()
