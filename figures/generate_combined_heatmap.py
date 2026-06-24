import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .generate_df import produce_df_results


def combined_heatmap(
    n_sources: int = 13,
    rel_mean_max: float = 0.65,
    rel_range: float = 0.2,
    restricted_list: list[int] = [10, 30, 50, 70, 90],
    heuristic_size: int | list[int] = 5,
    measure: str = "absolute",
    show_cbar: bool = True,
    show: bool = False,
    filename: str | None = None,
):
    """Plot a heatmap comparing all group types against the diverse deliberation
    baseline.

    Rows are reliability mean values (descending), columns are group types (expert
    deliberation + restricted aggregation groups). Cell values are the difference
    between a group's median accuracy and the diverse deliberation median for the same
    parameter setting. The best-performing group in each row is marked with an asterisk.

    Args:
        n_sources: Number of sources to load data for.
        rel_mean_max: Upper bound for reliability mean values shown.
        restricted_list: Which restricted-group percentile thresholds to include.
        heuristic_size: Heuristic size(s) to filter on when loading data.
        measure: "absolute" for percentage-point difference, "relative" for error
            reduction as a percentage of the remaining error.
        show_cbar: If True, includes a color bar.
        show: If True, displays the plot interactively after saving.
        filename: Output path without extension. Saves .eps and .png. Defaults to
            "figures/images/heatmap_combined_{n_sources}_{measure}".
    """
    df = produce_df_results(
        procedure_list=["deliberation", "aggregation"],
        heuristic_size=heuristic_size,
        reliability_range=rel_range,
        n_sources_list=[n_sources],
    )

    df_delib = df[df["procedure"] == "deliberation"]
    df_agg = df[df["procedure"] == "aggregation"]

    restricted_list_sorted = sorted(restricted_list)
    group_labels = ["expert (delib)"] + [
        f"restricted_{r}" for r in restricted_list_sorted
    ]

    rel_means = sorted(
        [rm for rm in df["reliability_mean"].unique() if rm <= rel_mean_max],
        reverse=True,
    )

    plt.rcParams.update(
        {
            "text.usetex": True,
            "text.latex.preamble": r"\usepackage{mathptmx}",
            "font.family": "serif",
            "font.size": 9.75,
        }
    )

    n_groups = len(group_labels)
    fig, ax = plt.subplots(figsize=(1.5 + 0.6 * n_groups, 0.6 + 0.5 * len(rel_means)))

    vmax = 10 if measure == "absolute" else 100

    rows = []
    for rel_mean in rel_means:
        diverse_vals = df_delib[
            (df_delib["group_type"] == "diverse")
            & (df_delib["reliability_mean"] == rel_mean)
        ]["accuracy"]
        diverse_med = diverse_vals.median()

        row = {}
        for label in group_labels:
            if label == "expert (delib)":
                vals = df_delib[
                    (df_delib["group_type"] == "expert")
                    & (df_delib["reliability_mean"] == rel_mean)
                ]["accuracy"]
            else:  # e.g. "restricted_10"
                vals = df_agg[
                    (df_agg["group_type"] == label)
                    & (df_agg["reliability_mean"] == rel_mean)
                ]["accuracy"]

            if measure == "absolute":
                row[label] = 100 * (vals.median() - diverse_med)
            else:
                diff = vals.median() - diverse_med
                if diverse_med < 1:
                    row[label] = 100 * (diff / (1 - diverse_med))
                else:
                    row[label] = float("nan")

        rows.append(row)

    pivot_df = pd.DataFrame(rows, index=rel_means, columns=group_labels)

    annot_df = pivot_df.copy().astype(object)
    for row_idx in pivot_df.index:
        best_col = pivot_df.loc[row_idx].idxmax()
        for c in pivot_df.columns:
            val = pivot_df.loc[row_idx, c]
            if pd.isna(val):
                annot_df.loc[row_idx, c] = ""
                continue
            val_r = round(val, 1)
            if val_r == 0.0:
                fmt = "0.0"
            elif val_r > 0:
                fmt = f"+{val_r:.1f}"
            else:
                fmt = f"{val_r:.1f}"
            if c == best_col:
                fmt += "*"
            annot_df.loc[row_idx, c] = fmt

    heatmap_params = {
        "cmap": "gray_r",
        "square": False,
        "cbar": show_cbar,
        "cbar_kws": {"shrink": 1.0},
        "vmin": 0,
        "vmax": vmax,
        "fmt": "",
        "annot": annot_df,
    }

    sns.heatmap(abs(pivot_df), ax=ax, **heatmap_params)

    ax.set_xlabel("")
    ax.set_ylabel("Reliability\n(mean)")
    ax.set_xticklabels(
        [
            label.replace("restricted_", "")
            .replace("expert (delib)", "expert\n(delib)")
            .replace("0", "0th")
            for label in group_labels
        ],
        rotation=0,
        # ha="right",
    )
    ax.set_yticklabels([f"{rm:.2f}" for rm in rel_means], rotation=0)

    # Bracket under restricted group columns (index 1 onward)
    n_grps = len(group_labels)
    x_left = 1 / n_grps
    x_right = 1.0
    x_mid = (x_left + x_right) / 2
    y_line = -0.45  # axes fraction: below the x-tick labels
    cap = 0.05

    kw = dict(transform=ax.transAxes, color="black", lw=0.8, clip_on=False)
    ax.plot([x_left, x_right], [y_line, y_line], **kw)
    ax.plot([x_left, x_left], [y_line, y_line + cap], **kw)
    ax.plot([x_right, x_right], [y_line, y_line + cap], **kw)
    ax.plot([x_mid, x_mid], [y_line, y_line - cap], **kw)
    ax.text(
        x_mid,
        y_line - 2 * cap,
        "Epistemic threshold (percentile)",
        ha="center",
        va="top",
        # fontsize=8,
        transform=ax.transAxes,
        clip_on=False,
    )

    plt.tight_layout()

    if filename is None:
        filename = f"figures/images/heatmap_combined_{n_sources}_{measure}"
    plt.savefig(f"{filename}.eps", bbox_inches="tight", dpi=800, format="eps")
    plt.savefig(f"{filename}.png", bbox_inches="tight", dpi=800)
    if show:
        plt.show()
    plt.close()
