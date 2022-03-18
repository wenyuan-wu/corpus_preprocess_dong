import os
from tqdm import tqdm
import pandas as pd
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )

def get_keywords_list(keyword_folder):
    keyword_list = []
    


def main():
    # adjust the following variable values to get the desired output
    file_folder = "output_data"
    days = "10D"
    output_folder = "data_by_10D"
    sorted_df = get_date_df(file_folder, days)
    creat_data(sorted_df, output_folder, file_folder)


if __name__ == '__main__':
    main()
