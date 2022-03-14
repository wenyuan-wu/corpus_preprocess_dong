import os
from tqdm import tqdm
import datetime
import pandas as pd
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def get_date_df(file_folder, days):
    process_bar = tqdm(os.listdir(file_folder))
    date_list = []
    name_list = []
    for file_name in process_bar:
        process_bar.set_description("Processing {}".format(file_name))
        paper_date = file_name[:10]
        paper_name = file_name
        date_list.append(paper_date)
        name_list.append(paper_name)
    dates_list = [date_list, name_list]
    df = pd.DataFrame(dates_list)
    df = df.transpose()
    df.columns = ['Date', 'File_name']
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by=['Date'], inplace=True)
    print(df)


def main():
    file_folder = "output_data"
    days = 10
    get_date_df(file_folder, days)


if __name__ == '__main__':
    main()
