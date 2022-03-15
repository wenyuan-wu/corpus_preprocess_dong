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
    df.columns = ['date', 'file_name']
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['date'], inplace=True)
    first_date = df.iloc[0]['date']
    first_year = first_date.year
    new_year = pd.Timestamp(f'{first_year}-01-01T00')
    if first_date == new_year:
        logging.info(f"The first day of year {first_year} already exists!")
    else:
        logging.info(f"Creating placeholder data for the first day of year {first_year}")
        df.loc[-1] = [new_year, 'placeholder.txt']
        df.index = df.index + 1
        df = df.sort_index()
    t = df.groupby(pd.Grouper(key="date", axis=0, freq=days, sort=True))['file_name'].apply(list).reset_index(
        name='file_name_list')
    t.to_csv("sorted_df.csv")
    return t


def creat_data(sorted_df, output_folder, file_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for idx, row in tqdm(sorted_df.iterrows()):
        if row['file_name_list']:
            date = row['date'].date()
            file_name_list = row['file_name_list']
            if not file_name_list[0] == 'placeholder.txt':
                text_str = []
                for file_name in file_name_list:
                    file_path = os.path.join(file_folder, file_name)
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        for line in infile:
                            text_str.append(line)
                out_file_path = os.path.join(output_folder, f"{date}.txt")
                with open(out_file_path, 'w', encoding='utf-8') as out_file:
                    out_file.write("".join(text_str))


def main():
    # adjust the following variable values to get the desired output
    file_folder = "output_data"
    days = "10D"
    output_folder = "data_by_10D"
    sorted_df = get_date_df(file_folder, days)
    creat_data(sorted_df, output_folder, file_folder)


if __name__ == '__main__':
    main()
