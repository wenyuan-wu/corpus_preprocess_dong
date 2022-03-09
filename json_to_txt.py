import pandas as pd
from tqdm import tqdm
import os
import json
import datetime
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def get_pmc_date(meta_folder_name, meta_file_name):
    """
    Function to load dataframe file from meta data.
    :param meta_folder_name: string, folder name of meta data
    :param meta_file_name: string, file name of meta data
    :return: pandas dataframe
    """
    file_path = os.path.join(meta_folder_name, meta_file_name)
    logging.info("loading meta data from {}".format(file_path))
    df = pd.read_csv(file_path, sep=';')
    return df


def prepare_data(json_folder_name, pmc_date_df, output_folder_name, date_form):
    """
    Function to prepare data for further process.
    :param json_folder_name: folder name of raw json files
    :param pmc_date_df: pandas dataframe of pmc metadata
    :param output_folder_name: folder name of output files
    :param date_form: format of date for output file names
    :return: None
    """
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)
    logging.info("loading json files from the folder {}".format(json_folder_name))
    process_bar = tqdm(os.listdir(json_folder_name))
    counter = 0
    for file_name in process_bar:
        process_bar.set_description("Processing {}".format(file_name))
        file_path = os.path.join(json_folder_name, file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
            paper_id = data["paper_id"]
            text_list = []
            for i in data["body_text"]:
                text_list.append(i["text"])
        paper_date = pmc_date_df.loc[pmc_date_df["pmcid"] == paper_id]["publish_time"].values[0]
        paper_date = datetime.datetime.strptime(paper_date, '%d.%m.%Y').strftime(date_form)
        out_file_name = paper_date + "_" + paper_id + ".txt"
        out_file_path = os.path.join(output_folder_name, out_file_name)
        with open(out_file_path, 'w') as out_file:
            out_file.write("\n".join(text_list))
        counter += 1
    logging.info("{} files successfully processed in {}".format(counter, output_folder_name))


def main():
    # adjust the following variable values to get the desired output
    meta_folder_name = "meta_data"
    meta_file_name = "pmc_date.csv"
    json_folder_name = "json_data"
    output_folder_name = "output_data"
    date_form = "%Y-%m-%d"

    pmc_date_df = get_pmc_date(meta_folder_name, meta_file_name)
    prepare_data(json_folder_name, pmc_date_df, output_folder_name, date_form)


if __name__ == '__main__':
    main()
