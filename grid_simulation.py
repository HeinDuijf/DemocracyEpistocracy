from datetime import datetime

import pandas as pd
import pytz
from IPython.display import display

from simulation import Simulation


class GridSimulation:
    def __init__(
        self,
        procedures: list[str],
        group_types: list,
        n_sources_list: list,
        reliability_distribution_list: list,
        n_samples: int,
        heuristic_size: int | list = 5,
        group_size: int = 9,
        estimate_sample_size: int | None = None,
    ):
        self.procedures = procedures
        self.group_types = group_types
        self.n_sources_list = n_sources_list
        self.reliability_distribution_list = reliability_distribution_list
        self.n_samples = n_samples
        self.heuristic_size = heuristic_size
        self.group_size = group_size
        self.estimate_sample_size = estimate_sample_size

    def run(self):
        timezone = pytz.timezone("Europe/Brussels")
        starttime = datetime.now(timezone).strftime("%H:%M:%S")
        print(f"Starting grid simulation at {starttime} with the following parameters:")

        params_df = self.create_parameter_df()
        display(params_df)
        total = len(params_df)
        for idx, params in params_df.iterrows():
            # convert to dict and turn NaN values into None
            params_dict = params.where(pd.notnull(params), None).to_dict()
            print(f"Running simulation {idx + 1} out of {total}...")
            Simulation(**params_dict).run()

        endtime = datetime.now(timezone).strftime("%H:%M:%S")
        print(f"Finished grid simulation at {endtime}.")

    def create_parameter_df(self):
        data = [
            {
                "procedures": self.procedures,
                "group_types": self.group_types,
                "n_sources": n_sources,
                "reliability_distribution": rel_dist,
                "heuristic_size": self.heuristic_size,
                "group_size": self.group_size,
                "n_samples": self.n_samples,
                "estimate_sample_size": None,
            }
            for n_sources in self.n_sources_list
            for rel_dist in self.reliability_distribution_list
        ]
        for item in data:
            if item["n_sources"] > 20:
                item["estimate_sample_size"] = self.estimate_sample_size
        return pd.DataFrame(data=data)


if __name__ == "__main__":
    GridSimulation(
        procedures=["aggregation", "deliberation"],
        group_types=["expert", "diverse"],
        n_sources_list=[13],
        reliability_distribution_list=[("equi", rel_mean, 0.2) for rel_mean in [0.55]],
        n_samples=5,
        estimate_sample_size=5,
    ).run()
