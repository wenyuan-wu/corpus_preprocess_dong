import pandas as pd
from tqdm import tqdm
import os


def get_pmc_date(file_name):
    folder_name = "meta_data"
    file_path = os.path.join(folder_name, file_name)
    df = pd.read_csv(file_path, sep=";")
    return df


def unicode_converter():
    raise NotImplementedError


def main():
    pmc_date_df = get_pmc_date("pmc_date.csv")
    print(pmc_date_df)
    print(pmc_date_df.columns)
    print(pmc_date_df["publish_time"])


if __name__ == '__main__':
    main()
