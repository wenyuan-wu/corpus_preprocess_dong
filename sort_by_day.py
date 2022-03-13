import os
from tqdm import tqdm
import datetime


def sort_by_day(file_folder, days):
    process_bar = tqdm(os.listdir(file_folder))
    counter = 0
    for file_name in process_bar:
        process_bar.set_description("Processing {}".format(file_name))
        # print(file_name)
        paper_date = datetime.datetime.strptime(file_name[:10], '%Y-%m-%d')
        print(paper_date)
        margin = datetime.timedelta(days=days)
        print(margin)
        new_date = paper_date + margin
        print(new_date)


def main():
    file_folder = "output_data"
    days = 10
    sort_by_day(file_folder, days)


if __name__ == '__main__':
    main()
