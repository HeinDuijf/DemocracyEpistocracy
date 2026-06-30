from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data"


def produce_df_results(
    procedure_list: list[str] = ["deliberation", "aggregation"],
    heuristic_size: int | list[int] = 5,
    reliability_range: float = 0.2,
    n_sources_list: list[int] = [13, 17],
    date: str = "",
) -> pd.DataFrame:
    files = [
        file
        for file in DATA_DIR.iterdir()
        if file.stem.split("_")[0] == "simulation"
        and date in file.stem.split("_")[1] + file.stem.split("_")[2]
    ]
    heuristic_str: str | int = heuristic_size  # type: ignore
    if isinstance(heuristic_size, list):
        heuristic_str = str(heuristic_str)[1:-1].replace(", ", "-")  # type: ignore

    dfs = []
    for file in files:
        df = pd.read_csv(file, index_col=0)
        if (
            heuristic_str in df.heuristic_size.values
            and reliability_range in df.reliability_range.values
        ):
            df = df[df["procedure"].isin(procedure_list)]
            df = df[df["n_sources"].isin(n_sources_list)]
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


GROUP_COLS = [
    "group_size",
    "n_sources",
    "heuristic_size",
    "reliability_mean",
    "reliability_range",
    "n_samples",
    "group_type",
    "procedure",
]


def aggregate_df_results(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(GROUP_COLS, as_index=False)["accuracy"].agg(
        accuracy_median="median", accuracy_mean="mean"
    )
