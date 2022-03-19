import os
from tqdm import tqdm
import pandas as pd
import logging
import re

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def get_sum_freq(input_folder, output_folder):
    process_bar = tqdm(os.listdir(input_folder))
    df_dict = {}
    for file_name in process_bar:
        process_bar.set_description("Processing {}".format(file_name))
        file_path = os.path.join(input_folder, file_name)
        df = pd.read_excel(file_path)
        date = get_date(file_name)
        type_list = df['Type'].unique()
        df_dict[f"{date}"] = {}
        for t in type_list:
            # print(t)
            # print(df.loc[df["Type"] == t])
            raw = df.loc[df["Type"] == t]["Relative frequency (focus)"].sum()
            # print(raw)
            norm = df.loc[df["Type"] == t]["Score"].sum()
            # print(norm)
            df_dict[f"{date}"][f"type {t} raw"] = raw
            df_dict[f"{date}"][f"type {t} norm"] = norm
    sum_df = pd.DataFrame.from_dict(df_dict, orient='index')
    outfile_path = os.path.join(output_folder, "summary.xlsx")
    sum_df.to_excel(outfile_path)


def get_date(file_name):
    match_str = r"_\d{8}_"
    date_ext = re.findall(match_str, file_name)
    return date_ext[0][1:9]


def main():
    # adjust the following variable values to get the desired output
    # keywords should not start with kapital
    input_folder = "freq_data_type"
    output_folder = "term_freq_sum"

    get_sum_freq(input_folder, output_folder)


if __name__ == '__main__':
    main()
