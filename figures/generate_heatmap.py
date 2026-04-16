import matplotlib.pyplot as plt
import seaborn as sns
from .generate_df import produce_df_results


def heatmap(
    procedure: str = "deliberation",
    diverse_team_type: str = "diverse",
    heuristic_size: int | list[int] = 5,
    n_sources_list: list[int] = [13, 17],
    rel_mean_max: float = 0.65,
    measure: str = "absolute",
    colors: bool = False,
    show: bool = False,
    show_cbar: bool = True,
    filename: str | None = None,
):
    df = produce_df_results(
        procedure_list=[procedure],
        heuristic_size=heuristic_size,
        reliability_range=0.2,
        n_sources_list=n_sources_list,
    )
    df_expert = df[df["group_type"] == "expert"]
    df_diverse = df[df["group_type"] == diverse_team_type]
    for row in df.iterrows():
        if row[1]["group_type"] == "expert":
            rel_mean = row[1]["reliability_mean"]
            n_sources = row[1]["n_sources"]
            df_diverse = df[
                (df["group_type"] == diverse_team_type)
                & (df["reliability_mean"] == rel_mean)
                & (df["n_sources"] == n_sources)
            ]
            difference = df_diverse["accuracy"].median() - row[1]["accuracy"]
            error_reduction = 100 * (difference / (1 - row[1]["accuracy"]))
            df_expert.loc[row[0], "difference"] = difference
            df_expert.loc[row[0], "error_reduction"] = error_reduction

    df_expert = df_expert[df_expert["reliability_mean"] <= rel_mean_max]
    if measure == "absolute":
        df_expert["effect_percent"] = 100 * df_expert["difference"]
    if measure == "relative":
        df_expert["effect_percent"] = df_expert["error_reduction"]
    # df_dummy = df_expert[df_expert["group_type"] == "expert"]
    pivot_df = df_expert.pivot(
        index="reliability_mean",
        columns="n_sources",
        values="effect_percent",
    )
    pivot_df.sort_index(inplace=True, ascending=False)

    sns.set_style("white")
    plt.rcParams.update(
        {
            "text.usetex": True,
            "text.latex.preamble": r"\usepackage{mathptmx}",
            "font.family": "serif",
            "font.size": 9.75,
        }
    )
    # font_style = {"family": "Times New Roman", "size": 12}
    # plt.rc("font", **font_style)
    plt.figure(figsize=(3, 2))

    heatmap_params = {
        # "annot": True,
        "cmap": "gray_r",  # "coolwarm"
        "square": True,
        "cbar": show_cbar,
        "cbar_kws": {"shrink": 1.0},
        "vmin": 0,
        "vmax": 10,
        "fmt": "",
    }
    df_heatmap = abs(pivot_df)
    annot_df = pivot_df.copy().map(lambda x: f"{x:.1f}")

    if colors:
        heatmap_params["cmap"] = "coolwarm"
        heatmap_params["center"] = 0
        df_heatmap = pivot_df

    if measure == "absolute":
        if colors:
            heatmap_params["vmin"] = -10
            heatmap_params["vmax"] = 10
        else:
            positives_df = pivot_df > 0.0
            annot_df[positives_df] = "+" + annot_df[positives_df]

    if measure == "relative":
        annot_df = pivot_df.copy().map(lambda x: f"{x:.0f}")
        heatmap_params["vmax"] = 100

        if colors:
            heatmap_params["vmin"] = -100
            heatmap_params["vmax"] = 100
        else:
            positives_df = pivot_df > 0.0
            annot_df[positives_df] = "+" + annot_df[positives_df]

    # effect_df = df.pivot(
    #     index="reliability_mean", columns="n_sources", values="effect_size"
    # )
    # effect_low = effect_df < 0.1
    # effect_mid = (effect_df >= 0.1) & (effect_df < 0.3)
    # annot_df[effect_low] = annot_df[effect_low] + "'"
    # annot_df[effect_mid] = annot_df[effect_mid] + "''"

    # pvalue_df = df.pivot(
    #     index="rel_mean",
    #     columns="n_sources",
    #     values="p_value",
    # )
    # if procedure == "deliberation":
    #     not_sig = df_heatmap == 0.0
    # else:
    #     not_sig = pvalue_df > 0.001
    # annot_df[not_sig] = ""

    heatmap_params["annot"] = annot_df

    fig = sns.heatmap(
        df_heatmap,
        **heatmap_params,
    )

    fig.set_xlabel(r"Sources (\#)")
    fig.set_ylabel("Reliability (mean)")
    plt.yticks(rotation=0)

    if filename is None:
        filename = f"figures/images/heatmap_{procedure}_{measure}"
    plt.savefig(
        f"{filename}.eps",
        bbox_inches="tight",
        dpi=800,
        format="eps",
    )
    plt.savefig(
        f"{filename}.png",
        bbox_inches="tight",
        dpi=800,
    )
    if show:
        plt.show()
    plt.close()
    plt.close()
