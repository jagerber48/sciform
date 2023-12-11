from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from tabulate import tabulate

if TYPE_CHECKING:
    from numpy.typing import NDArray


def quadratic(x: NDArray, c: float, x0: float, y0: float) -> NDArray:
    return (c / 2) * (x - x0) ** 2 + y0


def main() -> None:
    data_path = Path("data", "fit_data.json")
    with data_path.open() as f:
        data_dict = json.load(f)

    color_list = ["red", "blue", "purple"]
    fit_results_list = []

    fig, ax = plt.subplots(1, 1)

    for idx, single_data_dict in enumerate(data_dict.values()):
        x = single_data_dict["x"]
        y = single_data_dict["y"]
        y_err = single_data_dict["y_err"]

        fit_results_dict = {}

        color = color_list[idx]
        ax.errorbar(x, y, y_err, marker="o", linestyle="none", color=color, label=color)

        # noinspection PyTupleAssignmentBalance
        popt, pcov = curve_fit(quadratic, x, y, sigma=y_err, p0=(2e13, 0, 1e9))

        model_x = np.linspace(min(x), max(x), 100)
        model_y = quadratic(model_x, *popt)
        ax.plot(model_x, model_y, color=color)

        fit_results_dict["color"] = color

        fit_results_dict["curvature"] = popt[0]
        fit_results_dict["curvature_err"] = np.sqrt(pcov[0, 0])

        fit_results_dict["x0"] = popt[1]
        fit_results_dict["x0_err"] = np.sqrt(pcov[1, 1])

        fit_results_dict["y0"] = popt[2]
        fit_results_dict["y0_err"] = np.sqrt(pcov[2, 2])

        fit_results_list.append(fit_results_dict)

    ax.grid(True)  # noqa: FBT003
    ax.legend()

    fig.savefig("outputs/fit_plot_no_sciform.png", facecolor="white")
    plt.show()

    table_str = tabulate(
        fit_results_list,
        tablefmt="grid",
        headers="keys",
        floatfmt="#.2g",
    )
    table_path = Path("outputs", "fit_plot_no_sciform_table.txt")
    with table_path.open("w") as f:
        f.write(table_str)
    print(table_str)  # noqa: T201


if __name__ == "__main__":
    main()
