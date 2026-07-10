import matplotlib.pyplot as plt
from matplotlib import colormaps

from utils.weighted_procedures import weight_distribution_df


def weights_lineplot(
    n_sources: int = 13,
    heuristic_size: int = 5,
    rel_mean: float = 0.6,
    rel_range: float = 0.2,
    group_types: list[str] = [f"restricted_{p}" for p in range(10, 100, 10)],
    show: bool = False,
    filename: str | None = None,
):
    df_weights = weight_distribution_df(
        n_sources=n_sources,
        heuristic_size=heuristic_size,
        rel_mean=rel_mean,
        rel_range=rel_range,
        group_types=group_types,
    )

    plt.rcParams.update(
        {
            "text.usetex": True,
            "text.latex.preamble": r"\usepackage{mathptmx}",
            "font.family": "serif",
            "font.size": 9.75,
        }
    )

    cmap = colormaps["gray_r"]
    fig, ax = plt.subplots(figsize=(5, 3))
    for i, group_type in enumerate(group_types):
        shade = 0.25 + 0.6 * (i / (len(group_types) - 1))
        sub = df_weights[df_weights["group_type"] == group_type]
        ax.plot(
            sub["source"],
            sub["weight_fraction"],
            color=cmap(shade),
            marker="o",
            markersize=3,
            label=group_type.split("_")[1],
        )

    ax.axhline(
        1 / n_sources,
        color="black",
        linestyle="--",
        linewidth=0.8,
        label="Equal weight",
    )

    ax.set_xlabel("Source (ranked by reliability, ascending)")
    ax.set_ylabel("Weight (fraction)")
    ax.set_xticks([])
    ax.legend(
        title="Epistemic threshold (percentile)",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
    )
    plt.tight_layout()
    if filename is None:
        filename = "figures/images/weights"
    plt.savefig(f"{filename}.eps", bbox_inches="tight", dpi=800, format="eps")
    plt.savefig(f"{filename}.png", bbox_inches="tight", dpi=800)
    if show:
        plt.show()
    plt.close()
