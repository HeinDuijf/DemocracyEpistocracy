import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from utils.weighted_procedures import weight_results_df


def line_plot_comparison_weighted_procedure(
    procedure_list: list[str] = ["deliberation", "aggregation"],
    heuristic_size: int | list[int] = 5,
    rel_mean_max: float = 0.6,
    reliability_range: float = 0.2,
    n_sources_list: list[int] = [13, 17],
    date: str = "",
    show_progress: bool = True,
    show: bool = False,
    filename: str | None = None,
):
    """Plot a line-plot comparing the accuracy difference between the weighted
    procedure and the deliberation baseline, across reliability mean values.

    Args:
        plot_df: DataFrame containing the data to plot.
        rel_mean_max: Upper bound for reliability mean values shown.
        show: If True, displays the plot interactively after saving.
        filename: Output path without extension. Saves .eps and .png. Defaults to
            "figures/images/accuracy_difference_vs_weights".
    """
    plot_df = weight_results_df(
        procedure_list=procedure_list,
        heuristic_size=heuristic_size,
        rel_mean_max=rel_mean_max,
        reliability_range=reliability_range,
        n_sources_list=n_sources_list,
        date=date,
        show_progress=show_progress,
    )
    plot_df["accuracy_diff_pp"] = 100 * plot_df["accuracy_diff"]
    plot_df["accuracy_diff_weights_pp"] = 100 * plot_df["accuracy_diff_weights"]

    translate_metrics = {
        "accuracy_diff": "Accuracy difference",
        "accuracy_diff_weights": "Approximation using weights",
    }

    plt.rcParams.update(
        {
            "text.usetex": True,
            "text.latex.preamble": r"\usepackage{mathptmx}",
            "font.family": "serif",
            "font.size": 9.75,
        }
    )

    plt.rcParams["axes.grid.axis"] = "y"

    rel_means_sorted = sorted(plot_df["reliability_mean"].unique())
    rel_mean_pos = {rm: i for i, rm in enumerate(rel_means_sorted)}

    n_sources_sorted = sorted(plot_df["n_sources"].unique())
    marker_map = {n_sources_sorted[0]: "o", n_sources_sorted[1]: "s"}
    offset_map = {n_sources_sorted[0]: -0.15, n_sources_sorted[1]: 0.15}

    fig, ax = plt.subplots(figsize=(5, 3))

    for n_sources in n_sources_sorted:
        sub = plot_df[plot_df["n_sources"] == n_sources]
        x = sub["reliability_mean"].map(rel_mean_pos) + offset_map[n_sources]
        ax.scatter(
            x,
            sub["accuracy_diff_pp"],
            marker=marker_map[n_sources],
            s=90,
            color="lightgray",
            alpha=0.6,
            zorder=2,
        )
        ax.scatter(
            x,
            sub["accuracy_diff_weights_pp"],
            marker=marker_map[n_sources],
            s=20,
            color="black",
            zorder=3,
        )

    ax.set_xticks(list(rel_mean_pos.values()))
    ax.set_xticklabels([f"{rm:.2f}" for rm in rel_means_sorted])
    ax.set_xlim(-0.6, len(rel_means_sorted) - 1 + 0.6)
    ax.set_xlabel("Reliability (mean)")
    ax.set_ylabel("Accuracy difference (pp)")
    ax.margins(y=0.1)
    ax.set_ylim(bottom=0)

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor="lightgray",
            markersize=9,
            alpha=0.6,
            label=translate_metrics["accuracy_diff"],
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor="black",
            markersize=4,
            label=translate_metrics["accuracy_diff_weights"],
        ),
        Line2D(
            [0],
            [0],
            marker=marker_map[n_sources_sorted[0]],
            color="none",
            markerfacecolor="lightgray",
            markersize=7,
            label=f"{n_sources_sorted[0]} sources",
        ),
        Line2D(
            [0],
            [0],
            marker=marker_map[n_sources_sorted[1]],
            color="none",
            markerfacecolor="lightgray",
            markersize=7,
            label=f"{n_sources_sorted[1]} sources",
        ),
    ]
    ax.legend(handles=legend_handles, loc="center left", bbox_to_anchor=(1.02, 0.5))

    plt.tight_layout()
    if filename is None:
        filename = "figures/images/accuracy_difference_vs_weights"
    plt.savefig(
        f"{filename}.eps", bbox_inches="tight", pad_inches=0.3, dpi=800, format="eps"
    )
    plt.savefig(f"{filename}.png", bbox_inches="tight", pad_inches=0.3, dpi=800)
    if show:
        plt.show()
    plt.close()
