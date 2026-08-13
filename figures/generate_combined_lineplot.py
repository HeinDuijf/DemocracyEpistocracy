import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.lines import Line2D

from .generate_df import produce_df_results

LOOSELY_DOTTED = (0, (1, 10))


def combined_lineplot(
    n_sources_list: list[int] = [13, 17],
    rel_mean_max: float = 0.65,
    rel_range: float = 0.2,
    restricted_list: list[int] = list(range(10, 100, 10)),
    heuristic_size: int | list[int] = 5,
    measure: str = "absolute",
    show_aggregation: bool = True,
    show: bool = False,
    filename: str | None = None,
):
    """Plot a line-plot comparing all group types against the diverse deliberation
    baseline.

    Shows one line per (reliability mean, number of sources) combination, plotted
    across the epistemic threshold (percentile) of restricted aggregation groups, plus
    a horizontal dotted line per combination marking the expert deliberation baseline
    (which is not threshold-dependent). Color encodes reliability mean, linewidth
    encodes number of sources, and the dotted linestyle marks the expert (delib)
    baseline lines.

    Args:
        n_sources_list: Number-of-sources values to include (one linewidth each).
        rel_mean_max: Upper bound for reliability mean values shown.
        restricted_list: Which restricted-group percentile thresholds to include.
        heuristic_size: Heuristic size(s) to filter on when loading data.
        measure: "absolute" for percentage-point difference, "relative" for error
            reduction as a percentage of the remaining error.
        show_aggregation: If False, hides the epistocratic-aggregation lines (and
            their legend entry) while keeping the x/y limits identical to the
            show_aggregation=True version.
        show: If True, displays the plot interactively after saving.
        filename: Output path without extension. Saves .eps and .png. Defaults to
            "figures/images/lineplot_combined_{n_sources_list}_{measure}".
    """
    n_sources_sorted = sorted(n_sources_list)

    df = produce_df_results(
        procedure_list=["deliberation", "aggregation"],
        heuristic_size=heuristic_size,
        reliability_range=rel_range,
        n_sources_list=n_sources_sorted,
    )

    df_delib = df[df["procedure"] == "deliberation"]
    df_agg = df[df["procedure"] == "aggregation"]

    restricted_list_sorted = sorted(restricted_list)

    rel_means = sorted(
        [rel_mean for rel_mean in df["reliability_mean"].unique() if rel_mean <= rel_mean_max],
        reverse=False,
    )

    plt.rcParams.update(
        {
            "text.usetex": True,
            "text.latex.preamble": r"\usepackage{mathptmx}",
            "font.family": "serif",
            "font.size": 9.75,
        }
    )

    _, ax = plt.subplots(figsize=(3.5, 3.5))

    cmap = colormaps["gray_r"]
    n_rel_means = len(rel_means)
    linewidths = [1.2 + 1.3 * i for i in range(len(n_sources_sorted))]

    for rel_mean_idx, rel_mean in enumerate(rel_means):
        shade = 0.25 + 0.6 * (rel_mean_idx / max(n_rel_means - 1, 1))
        color = cmap(shade)

        for n_sources, linewidth in zip(n_sources_sorted, linewidths):
            df_delib_n = df_delib[df_delib["n_sources"] == n_sources]
            df_agg_n = df_agg[df_agg["n_sources"] == n_sources]

            diverse_vals = df_delib_n[
                (df_delib_n["group_type"] == "diverse")
                & (df_delib_n["reliability_mean"] == rel_mean)
            ]["accuracy"]
            diverse_med = diverse_vals.median()

            def compute_value(vals, diverse_med=diverse_med):
                if measure == "absolute":
                    return 100 * (diverse_med - vals.median())
                return float("nan")

            expert_vals = df_delib_n[
                (df_delib_n["group_type"] == "expert")
                & (df_delib_n["reliability_mean"] == rel_mean)
            ]["accuracy"]
            expert_value = compute_value(expert_vals)

            y_values = []
            for epistemic_threshold in restricted_list_sorted:
                vals = df_agg_n[
                    (df_agg_n["group_type"] == f"restricted_{epistemic_threshold}")
                    & (df_agg_n["reliability_mean"] == rel_mean)
                ]["accuracy"]
                y_values.append(compute_value(vals))

            ax.plot(
                restricted_list_sorted,
                y_values,
                color=color,
                linewidth=linewidth,
                marker="o",
                markersize=3,
                alpha=1 if show_aggregation else 0,
            )
            ax.axhline(expert_value, color=color, linestyle=LOOSELY_DOTTED, linewidth=linewidth)
            
    ax.set_xticks(restricted_list_sorted)
    ax.set_xlabel("Epistemic threshold (percentile)")
    if measure == "absolute":
        ax.set_ylabel("Accuracy difference (pp)")
    else:
        ax.set_ylabel(r"Error reduction (\%)")
    ax.set_ylim(top=0)

    color_handles = [
        Line2D([0], [0], color=cmap(0.25 + 0.6 * (i / max(n_rel_means - 1, 1))))
        for i in range(n_rel_means)
    ]
    color_labels = [f"{rm:.2f}" for rm in rel_means]
    color_legend = ax.legend(
        color_handles,
        color_labels,
        title="Reliability (mean)",
        loc="center left",
        bbox_to_anchor=(1.02, 0.8),
        borderaxespad=0.0,
    )
    color_legend._legend_box.align = "left"
    ax.add_artist(color_legend)

    size_handles = [
        Line2D([0], [0], color="black", linewidth=lw) for lw in linewidths
    ] 
    size_labels = [str(n) for n in n_sources_sorted]
    size_legend = ax.legend(
        size_handles,
        size_labels,
        title=r"Sources (\#)",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0.0,
    )
    size_legend._legend_box.align = "left"
    ax.add_artist(size_legend)

    style_handles = [
        Line2D([0], [0], color="black", linestyle="solid", linewidth=1.2),
        Line2D([0], [0], color="black", linestyle=LOOSELY_DOTTED, linewidth=1.2)
    ]
    style_labels = ["epistocratic agg.", "expert delib."]
    style_legend = ax.legend(
        style_handles,
        style_labels,
        title="Institutions",
        loc="center left",
        bbox_to_anchor=(1.02, 0.2),
        borderaxespad=0.0,
    )
    style_legend._legend_box.align = "left"
    ax.add_artist(style_legend)

    plt.tight_layout()

    legend_artists = [color_legend, size_legend, style_legend]

    if filename is None:
        n_sources_str = "-".join(str(n) for n in n_sources_sorted)
        suffix = "" if show_aggregation else "_expert-delib-only"
        filename = f"figures/images/lineplot_combined_{n_sources_str}_{measure}{suffix}"
    plt.savefig(
        f"{filename}.eps",
        bbox_inches="tight",
        bbox_extra_artists=legend_artists,
        dpi=800,
        format="eps",
    )
    plt.savefig(
        f"{filename}.png",
        bbox_inches="tight",
        bbox_extra_artists=legend_artists,
        dpi=800,
    )
    if show:
        plt.show()
    plt.close()
