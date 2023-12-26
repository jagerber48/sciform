from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import matplotlib.pyplot as plt
import numpy as np
from sciform import Formatter
from scipy.optimize import curve_fit
from tabulate import tabulate

if TYPE_CHECKING:
    from numpy.typing import NDArray


def get_scale_and_offset_from_offset_str(
    ax: plt.Axes,
    axis: Literal["x", "y"],
) -> tuple[float, float]:
    """Get the scale and offset for an axis formatted in scientific mode."""
    plt.draw()
    if axis == "x":
        offset_text_obj = ax.xaxis.get_offset_text()
    elif axis == "y":
        offset_text_obj = ax.yaxis.get_offset_text()
    else:
        msg = f"axis must be 'x' or 'y', not '{axis}'."
        raise ValueError(msg)

    ax.ticklabel_format(axis=axis, style="sci")
    ax.get_figure().canvas.draw()  # Redraw canvas to update offset text
    offset_text = offset_text_obj.get_text()

    # Replace minus sign with hyphen minus sign
    offset_text = offset_text.replace("\u2212", "-")

    pattern = re.compile(r"^(?P<scale>1e[+-]?\d+)?(?P<offset>[+-]1e\d+)?$")
    match = re.match(pattern, offset_text)
    scale = float(match.group("scale") or 1)
    offset = float(match.group("offset") or 0)

    return scale, offset


def prefix_exp_ticks(
    ax: plt.Axes,
    axis: Literal["x", "y"],
    *,
    shifted: bool = False,
) -> None:
    """
    Use prefix notation for axis tick labels. Scale the tick labels by
    the multiplier that appears in the offset text and format the labels
    into SI prefix format. Format any remaining offset value in the
    offset text into SI prefix format as well.
    """
    if not shifted:
        exp_mode = "engineering"
    else:
        exp_mode = "engineering_shifted"
    # noinspection PyTypeChecker
    tick_formatter = Formatter(exp_mode=exp_mode, exp_format="prefix")
    # noinspection PyTypeChecker
    offset_formatter = Formatter(sign_mode="+", exp_mode=exp_mode, exp_format="prefix")

    ax.ticklabel_format(axis=axis, style="sci")

    if axis == "x":
        old_ticklabels = ax.get_xticklabels()
    elif axis == "y":
        old_ticklabels = ax.get_yticklabels()
    else:
        msg = f"axis must be 'x' or 'y', not '{axis}'."
        raise ValueError(msg)

    scale, offset = get_scale_and_offset_from_offset_str(ax, axis)

    new_tick_locations = []
    new_tick_labels = []
    for old_ticklabel in old_ticklabels:
        x, y = old_ticklabel.get_position()
        if axis == "x":
            new_tick_locations.append(x)
        else:
            new_tick_locations.append(y)

        # Replace minus sign with hyphen minus sign
        old_label_str = old_ticklabel.get_text().replace("\u2212", "-")
        val = float(old_label_str) * scale
        new_str = tick_formatter(val)
        new_tick_labels.append(new_str)

    if offset != 0:
        offset_str = offset_formatter(offset)
    else:
        offset_str = ""

    if axis == "x":
        ax.set_xticks(new_tick_locations, new_tick_labels)
        ax.text(x=1.01, y=0, s=offset_str, transform=ax.transAxes)
    else:
        ax.set_yticks(new_tick_locations, new_tick_labels)
        ax.text(x=0, y=1.01, s=offset_str, transform=ax.transAxes)


def quadratic(x: NDArray, c: float, x0: float, y0: float) -> NDArray:
    return (c / 2) * (x - x0) ** 2 + y0


def main() -> None:
    fit_results_formatter = Formatter(
        exp_mode="engineering",
        round_mode="sig_fig",
        paren_uncertainty=True,
        ndigits=2,
    )

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
        fit_results_dict["curvature"] = fit_results_formatter(
            popt[0],
            np.sqrt(pcov[0, 0]),
        )
        fit_results_dict["x0"] = fit_results_formatter(popt[1], np.sqrt(pcov[1, 1]))
        fit_results_dict["y0"] = fit_results_formatter(popt[2], np.sqrt(pcov[2, 2]))

        fit_results_list.append(fit_results_dict)

    ax.grid(True)  # noqa: FBT003
    ax.legend()

    prefix_exp_ticks(ax, "x")
    prefix_exp_ticks(ax, "y", shifted=True)

    fig.savefig("outputs/fit_plot_with_sciform.png", facecolor="white")
    plt.show()

    table_str = tabulate(fit_results_list, headers="keys", tablefmt="grid")
    table_path = Path("outputs", "fit_plot_with_sciform_table.txt")
    with table_path.open("w") as f:
        f.write(table_str)
    print(table_str)  # noqa: T201


if __name__ == "__main__":
    main()
