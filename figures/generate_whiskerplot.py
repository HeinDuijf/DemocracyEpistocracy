import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

from .generate_df import produce_df_results


def produce_whiskers_plot(
    df: pd.DataFrame | None = None,
    n_sources_list: list[int] = [13, 17],
    rel_mean_list: list[float] = [0.55, 0.6, 0.65],
    restricted_list: list[int] = [10, 30, 50, 70, 90],
    filename=None,
):
    """Plot accuracy ranges for aggregation and deliberation procedures.

    Produces a grid of whisker plots with rows for each number of sources and
    columns for each reliability mean. Each plot shows the min–max accuracy
    range per group type. The best and worst performing group in each facet are
    marked with an asterisk.

    Args:
        df: Simulation results. If None, loaded from the data folder via
            produce_df_results().
        n_sources_list: Number-of-sources values to include (one row each).
        rel_mean_list: Reliability mean values to include (one column each).
        restricted_list: Restricted-group sizes to include in the plot.
        filename: Output path without extension. Saves .eps and .png if given,
            otherwise displays interactively.
    """
    if df is None:
        df = produce_df_results()

    restricted_list_str = [str(r) for r in restricted_list]
    reliability_means = [
        rel_mean
        for rel_mean in sorted(df["reliability_mean"].unique())
        if rel_mean in rel_mean_list
    ]
    n_rows = len(n_sources_list)
    n_cols = len(reliability_means)

    plt.rcParams.update(
        {
            "text.usetex": True,
            "text.latex.preamble": r"\usepackage{mathptmx}",
            "font.family": "serif",
            "font.size": 9.75,
        }
    )

    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(2 + 3 * n_cols, 1 + 3 * n_rows),
        sharey="row",
        squeeze=False,
    )

    def draw_range(ax, vals, i, color):
        if len(vals) == 0:
            return
        cap, linewidth = 0.1, 1
        lo, hi = vals.min(), vals.max()
        if abs(hi - lo) < 1e-4:
            lo = hi
        ax.plot([lo, hi], [i, i], color=color, linewidth=linewidth)
        ax.plot([lo, lo], [i - cap, i + cap], color=color, linewidth=linewidth)
        ax.plot([hi, hi], [i - cap, i + cap], color=color, linewidth=linewidth)

    def make_yticklabels(categories):
        labels = []
        first_restricted = True
        for cat in categories:
            if cat == "expert (delib)":
                labels.append("expert (delib)")
            elif cat == "diverse":
                labels.append("diverse")
            elif first_restricted:
                labels.append(f"{cat.split('_')[-1]} restricted")
                first_restricted = False
            else:
                labels.append(cat.split("_")[-1])
        return labels

    for row, n_sources in enumerate(n_sources_list):
        df_row = df[df["n_sources"] == n_sources]
        agg = df_row[df_row["procedure"] == "aggregation"]
        delib = df_row[df_row["procedure"] == "deliberation"]

        group_types = [
            gt
            for gt in agg["group_type"].unique()
            if "restricted" not in gt or gt.split("_")[-1] in restricted_list_str
        ]
        agg_categories = sorted(
            group_types, key=lambda x: -1 if x == "diverse" else int(x.split("_")[-1])
        )
        categories = ["expert (delib)"] + agg_categories

        for col, rel_mean in enumerate(reliability_means):
            ax = axes[row, col]
            facet_agg = agg[agg["reliability_mean"] == rel_mean]
            facet_delib = delib[delib["reliability_mean"] == rel_mean]
            expert_vals = facet_delib[facet_delib["group_type"] == "expert"][
                "accuracy"
            ].dropna()

            max_by_type = facet_agg.groupby("group_type")["accuracy"].max()
            max_by_type["expert (delib)"] = expert_vals.max()
            best = max_by_type.idxmax()
            worst = max_by_type.idxmin()

            x_range = facet_agg["accuracy"].max() - facet_agg["accuracy"].min()
            x_offset = x_range * 0.02

            for i, cat in enumerate(categories):
                vals = (
                    expert_vals
                    if cat == "expert (delib)"
                    else facet_agg[facet_agg["group_type"] == cat]["accuracy"].dropna()
                )
                draw_range(ax, vals, i, "black")
                if len(vals) == 0:
                    continue
                if cat == best:
                    ax.text(
                        vals.max() + x_offset,
                        i,
                        "*",
                        va="center",
                        ha="left",
                        fontsize=10,
                    )
                elif cat == worst:
                    ax.text(
                        vals.min() - x_offset,
                        i,
                        "*",
                        va="center",
                        ha="right",
                        fontsize=10,
                    )

            ax.axhline(0.5, color="gray", linewidth=0.8, linestyle="--")
            ax.axhline(1.5, color="gray", linewidth=0.8, linestyle="--")
            ax.yaxis.grid(True, color="lightgray", linewidth=0.5, zorder=0)
            ax.set_axisbelow(True)
            locator = (
                MultipleLocator(0.02) if rel_mean == 0.55 else MultipleLocator(0.01)
            )
            ax.xaxis.set_major_locator(locator)
            ax.set_xlabel("Group reliability")

        # Right-side y-tick labels
        ax_right = axes[row, -1]
        ax_right.yaxis.set_label_position("right")
        ax_right.yaxis.set_ticks_position("right")
        ax_right.set_yticks(range(len(categories)))
        ax_right.set_yticklabels(make_yticklabels(categories), ha="left")

        # Row label (n_sources)
        axes[row, 0].annotate(
            str(n_sources),
            xy=(0, 0.5),
            xycoords="axes fraction",
            xytext=(-20, 0),
            textcoords="offset points",
            ha="center",
            va="center",
            fontsize=13,
            fontweight="bold",
        )

    plt.tight_layout()

    for row in range(n_rows - 1):
        for col in range(n_cols):
            axes[row, col].set_xlabel("")

    for ax in axes.flat:
        x_min, x_max = ax.get_xlim()
        margin = (x_max - x_min) * 0.05
        ax.set_xlim(x_min - margin, x_max + margin)

    for row in range(n_rows):
        for col in range(n_cols):
            plt.setp(axes[row, col].get_yticklabels(), visible=False)

    # Column titles
    for col, rel_mean in enumerate(reliability_means):
        axes[0, col].set_title(str(rel_mean), fontsize=13, fontweight="bold")

    single_cell = n_rows == 1 and n_cols == 1
    fig.text(
        0.4 if single_cell else 0.5,
        1.04 if single_cell else 1.02,
        "Source reliability (mean)",
        ha="center",
        va="bottom",
        fontsize=15,
        fontweight="bold",
    )
    fig.text(
        -0.08 if single_cell else 0.05,
        0.55 if single_cell else 0.5,
        r"Sources (\#)",
        ha="center",
        va="center",
        fontsize=15,
        fontweight="bold",
        rotation=90,
    )

    if filename:
        plt.savefig(f"{filename}.eps", bbox_inches="tight", dpi=800, format="eps")
        plt.savefig(f"{filename}.png", bbox_inches="tight", dpi=800)
    else:
        plt.show()
