import json

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tabulate import tabulate


def quadratic(x, c, x0, y0):
    return (c / 2) * (x - x0) ** 2 + y0


def main():
    with open('data/fit_data.json', 'r') as f:
        data_dict = json.load(f)

    color_list = ['red', 'blue', 'purple']
    fit_results_list = list()

    fig, ax = plt.subplots(1, 1)

    for idx, single_data_dict in enumerate(data_dict.values()):
        x = single_data_dict['x']
        y = single_data_dict['y']
        y_err = single_data_dict['y_err']

        fit_results_dict = dict()

        color = color_list[idx]
        ax.errorbar(x, y, y_err, marker='o', linestyle='none', color=color,
                    label=color)

        popt, pcov = curve_fit(quadratic, x, y, sigma=y_err, p0=(2e13, 0, 1e9))

        model_x = np.linspace(min(x), max(x), 100)
        model_y = quadratic(model_x, *popt)
        ax.plot(model_x, model_y, color=color)

        fit_results_dict['color'] = color

        fit_results_dict['curvature'] = popt[0]
        fit_results_dict['curvature_err'] = np.sqrt(pcov[0, 0])

        fit_results_dict['x0'] = popt[1]
        fit_results_dict['x0_err'] = np.sqrt(pcov[1, 1])

        fit_results_dict['y0'] = popt[2]
        fit_results_dict['y0_err'] = np.sqrt(pcov[2, 2])

        fit_results_list.append(fit_results_dict)

    ax.grid(True)
    ax.legend()

    fig.savefig('outputs/fit_plot_no_sciform.png', facecolor='white')
    plt.show()

    table_str = tabulate(fit_results_list, tablefmt='grid', headers='keys',
                         floatfmt='#.2g')
    with open('outputs/fit_plot_no_sciform_table.txt', 'w') as f:
        f.write(table_str)
    print(table_str)


if __name__ == "__main__":
    main()
