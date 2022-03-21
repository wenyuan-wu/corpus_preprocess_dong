import os
import numpy as np
import pandas as pd
import logging
import matplotlib.pyplot as plt
import math

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def tricubic(x):
    y = np.zeros_like(x)
    idx = (x >= -1) & (x <= 1)
    y[idx] = np.power(1.0 - np.power(np.abs(x[idx]), 3), 3)
    return y


class Loess(object):

    @staticmethod
    def normalize_array(array):
        min_val = np.min(array)
        max_val = np.max(array)
        return (array - min_val) / (max_val - min_val), min_val, max_val

    def __init__(self, xx, yy, degree=1):
        self.n_xx, self.min_xx, self.max_xx = self.normalize_array(xx)
        self.n_yy, self.min_yy, self.max_yy = self.normalize_array(yy)
        self.degree = degree

    @staticmethod
    def get_min_range(distances, window):
        min_idx = np.argmin(distances)
        n = len(distances)
        if min_idx == 0:
            return np.arange(0, window)
        if min_idx == n-1:
            return np.arange(n - window, n)

        min_range = [min_idx]
        while len(min_range) < window:
            i0 = min_range[0]
            i1 = min_range[-1]
            if i0 == 0:
                min_range.append(i1 + 1)
            elif i1 == n-1:
                min_range.insert(0, i0 - 1)
            elif distances[i0-1] < distances[i1+1]:
                min_range.insert(0, i0 - 1)
            else:
                min_range.append(i1 + 1)
        return np.array(min_range)

    @staticmethod
    def get_weights(distances, min_range):
        max_distance = np.max(distances[min_range])
        weights = tricubic(distances[min_range] / max_distance)
        return weights

    def normalize_x(self, value):
        return (value - self.min_xx) / (self.max_xx - self.min_xx)

    def denormalize_y(self, value):
        return value * (self.max_yy - self.min_yy) + self.min_yy

    def estimate(self, x, window, use_matrix=False, degree=1):
        n_x = self.normalize_x(x)
        distances = np.abs(self.n_xx - n_x)
        min_range = self.get_min_range(distances, window)
        weights = self.get_weights(distances, min_range)

        if use_matrix or degree > 1:
            wm = np.multiply(np.eye(window), weights)
            xm = np.ones((window, degree + 1))

            xp = np.array([[math.pow(n_x, p)] for p in range(degree + 1)])
            for i in range(1, degree + 1):
                xm[:, i] = np.power(self.n_xx[min_range], i)

            ym = self.n_yy[min_range]
            xmt_wm = np.transpose(xm) @ wm
            beta = np.linalg.pinv(xmt_wm @ xm) @ xmt_wm @ ym
            y = (beta @ xp)[0]
        else:
            xx = self.n_xx[min_range]
            yy = self.n_yy[min_range]
            sum_weight = np.sum(weights)
            sum_weight_x = np.dot(xx, weights)
            sum_weight_y = np.dot(yy, weights)
            sum_weight_x2 = np.dot(np.multiply(xx, xx), weights)
            sum_weight_xy = np.dot(np.multiply(xx, yy), weights)

            mean_x = sum_weight_x / sum_weight
            mean_y = sum_weight_y / sum_weight

            b = (sum_weight_xy - mean_x * mean_y * sum_weight) / \
                (sum_weight_x2 - mean_x * mean_x * sum_weight)
            a = mean_y - b * mean_x
            y = a + b * n_x
        return self.denormalize_y(y)


def read_sum_df(input_folder, file_name):
    filepath = os.path.join(input_folder, file_name)
    sum_df = pd.read_excel(filepath)
    sum_df['Unnamed: 0'] = sum_df['Unnamed: 0'].astype('string')
    return sum_df


def plot_data(sum_df, input_folder):
    type_list = ['type 1.0 norm',
                 'type 2.1 norm', 'type 2.2 norm', 'type 2.3 norm',
                 'type 3.1 norm', 'type 3.2 norm', 'type 3.3 norm',
                 'type 4.1 norm', 'type 4.2 norm']
    x_labels = sum_df['Unnamed: 0'].values
    for typ in type_list:
        y_org = sum_df[typ].values
        plot_loess(x_labels, y_org, input_folder, typ)


def plot_loess(x_labels, y_val, input_folder, plot_name):
    x_val = np.array(list(range(60)))
    loess = Loess(x_val, y_val)
    y_list = []

    for x in x_val:
        y = loess.estimate(x, window=7, use_matrix=False, degree=1)
        y_list.append(y)
    y_arr = np.array(y_list)
    plt.subplots(figsize=(15, 10))
    plt.scatter(x_val, y_arr)
    plt.plot(x_val, y_arr)
    plt.title(plot_name)
    plt.xticks(x_val, x_labels, rotation=75)
    file_path = os.path.join(input_folder, f"{plot_name}.png")
    plt.savefig(file_path)
    logging.info(f"figure saved in {file_path}")


def main():
    # adjust the following variable values to get the desired output
    # keywords should not start with kapital
    summary_file = "summary_socialmedia.xlsx"
    input_folder = "summary_data"
    sum_df = read_sum_df(input_folder, summary_file)
    plot_data(sum_df, input_folder)


if __name__ == '__main__':
    main()
