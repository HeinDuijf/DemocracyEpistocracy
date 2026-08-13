import pandas as pd
from tqdm.auto import tqdm

from figures.generate_df import aggregate_df_results, produce_df_results
from models.generate_teams import generate_qualified_heuristics
from models.sources import Sources
from utils.basic_functions import calculate_competence_with_duplicates


def calculate_weights(
    n_sources, heuristic_size, rel_mean, rel_range, group_type, procedure
) -> dict | None:
    """Calculates the weights of sources based on how frequently they are accessed by
    all admissible heuristics in the specified parameters.

    Note: Only works for aggregation procedure, returns None for deliberation procedure.
    """
    sources = Sources(n_sources, reliability_distribution=("equi", rel_mean, rel_range))
    weights_dict = {source: 0 for source in sources.sources}
    if procedure == "deliberation":
        return None

    if group_type == "diverse":
        qualifying_percentile = 0
    else:
        qualifying_percentile = int(group_type.split("_")[1])

    qualified_agents = generate_qualified_heuristics(
        sources=sources,
        heuristic_size=heuristic_size,
        qualifying_percentile=qualifying_percentile,
    )

    for agent in qualified_agents:
        for source in agent.heuristic:
            weights_dict[source] += 1
    return weights_dict


def calculate_weighted_result(
    n_sources, heuristic_size, rel_mean, rel_range, group_type, procedure
) -> float | None:
    """Calculates the result of the weighted procedure, where the source weights are
    based on how frequently they were accessed by all admissible heuristics in the
    specified parameters.

    Note: Only works for aggregation procedure, returns None for deliberation procedure.
    """
    sources = Sources(n_sources, reliability_distribution=("equi", rel_mean, rel_range))
    weights_dict = calculate_weights(
        n_sources, heuristic_size, rel_mean, rel_range, group_type, procedure
    )
    if weights_dict is None:
        return None
    weighted_result, _ = calculate_competence_with_duplicates(
        sources.reliabilities, list(weights_dict.values())
    )
    return weighted_result


def weight_distribution_df(
    n_sources: int = 13,
    heuristic_size: int = 5,
    rel_mean: float = 0.6,
    rel_range: float = 0.2,
    group_types: list[str] = [f"restricted_{p}" for p in range(10, 100, 10)],
    procedure="aggregation",
) -> pd.DataFrame:
    """Calculates the weight distribution of sources based on how frequently they are
    accessed by all admissible heuristics, across group types."""
    rows = []
    for group_type in group_types:
        weights_dict = calculate_weights(
            n_sources, heuristic_size, rel_mean, rel_range, group_type, procedure
        )
        total = sum(weights_dict.values())
        for source, weight in weights_dict.items():
            rows.append(
                {
                    "source": source,
                    "group_type": group_type,
                    "weight_fraction": weight / total,
                }
            )
    return pd.DataFrame(rows)


def weight_results_df(
    procedure_list: list[str] = ["deliberation", "aggregation"],
    heuristic_size: int | list[int] = 5,
    rel_mean_max: float = 0.6,
    reliability_range: float = 0.2,
    n_sources_list: list[int] = [13, 17],
    date: str = "",
    show_progress: bool = True,
) -> pd.DataFrame:
    """Calculates the accuracy difference between the weighted procedure and the
    deliberation baseline, across reliability mean values and number of sources."""
    df = aggregate_df_results(
        produce_df_results(
            procedure_list=procedure_list,
            heuristic_size=heuristic_size,
            reliability_range=reliability_range,
            n_sources_list=n_sources_list,
            date=date,
        )
    )

    iterable = df.iterrows()
    if show_progress:
        iterable = tqdm(iterable, total=len(df), desc="Calculating weighted results")

    for k, row in iterable:
        weighted_result = calculate_weighted_result(
            n_sources=row["n_sources"],
            rel_mean=row["reliability_mean"],
            rel_range=row["reliability_range"],
            heuristic_size=row["heuristic_size"],
            group_type=row["group_type"],
            procedure=row["procedure"],
        )
        df.loc[k, "accuracy_calculated"] = (
            float(weighted_result) if weighted_result is not None else None
        )

    join_keys = ["n_sources", "reliability_mean", "heuristic_size", "reliability_range"]

    baseline_median = df.loc[
        (df["group_type"] == "diverse") & (df["procedure"] == "deliberation"),
        join_keys + ["accuracy_median"],
    ].rename(columns={"accuracy_median": "baseline_accuracy_median"})

    df = df.drop(columns=["baseline_accuracy_median"], errors="ignore").merge(
        baseline_median, on=join_keys, how="left"
    )

    df["accuracy_diff"] = (
        df["baseline_accuracy_median"] 
        - pd.to_numeric(df["accuracy_median"], errors="coerce") 
    )
    df["accuracy_diff_weights"] = (
        df["baseline_accuracy_median"]
        - pd.to_numeric(df["accuracy_calculated"], errors="coerce")
    )

    df["accuracy_diff_weights"] = df["accuracy_diff_weights"].round(6)
    df = df.loc[
        (df["procedure"] == "aggregation") & (df["group_type"] != "diverse")
    ].copy()
    df = df.dropna(subset=["accuracy_diff", "accuracy_diff_weights"])
    df = df[df["reliability_mean"] <= rel_mean_max]
    return df
