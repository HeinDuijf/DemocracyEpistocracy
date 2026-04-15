import copy
import itertools as it
import time
from concurrent.futures import ProcessPoolExecutor as Pool
from functools import partial

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

from models.generate_teams import (
    generate_diverse_team,
    generate_expert_team,
    generate_random_crowd,
    generate_restricted_team,
)
from models.sources import Sources


class Simulation:
    def __init__(
        self,
        filename_csv: str | None = None,
        procedures: list[str] = ["deliberation"],
        # outcomes: list[str] = ["opinion", "evidence", "bounded"],
        group_types: list = ["expert", "diverse"],
        n_sources: int = 13,
        reliability_distribution=("equidist", 0.6, 0.2),
        heuristic_size: int = 5,
        group_size: int = 9,
        n_samples: int = 10**3,
        estimate_sample_size: int | None = None,
    ):
        time_str = time.strftime("%Y%m%d_%H%M%S")
        self.filename_csv = filename_csv
        if filename_csv is None:
            self.filename_csv = f"data/simulation_{time_str}.csv"
        self.sources = Sources(
            n_sources=n_sources, reliability_distribution=reliability_distribution
        )
        self.n_sources = n_sources
        self.reliability_distribution = reliability_distribution

        self.group_types = group_types
        self.heuristic_size = heuristic_size
        self.group_size = group_size
        self.n_samples = n_samples
        self.estimate_sample_size = estimate_sample_size
        self.procedures = procedures

    def run(self):
        results_aggregation = None
        results_deliberation = None

        # Run simulations in parallel for aggregation
        if "aggregation" in self.procedures:
            team_simulate_aggregation = partial(
                self.group_simulate, procedure="aggregation"
            )
            with Pool() as pool:
                params, total = self.get_params()
                results_aggregation = pd.DataFrame(
                    tqdm(
                        pool.map(team_simulate_aggregation, params),
                        total=total,
                        desc="Calculating/estimating aggregation results",
                    )
                )

        # Run simulations in parallel for deliberation
        if "deliberation" in self.procedures:
            with Pool() as pool:
                team_simulate_deliberation = partial(
                    self.group_simulate, procedure="deliberation"
                )
                total = len(self.group_types)
                results_deliberation = pd.DataFrame(
                    tqdm(
                        pool.map(team_simulate_deliberation, self.group_types),
                        total=total,
                        desc="Calculating deliberation results",
                    )
                )

        # Merge results
        if "aggregation" in self.procedures and "deliberation" in self.procedures:
            results = pd.concat(
                [results_aggregation, results_deliberation], ignore_index=True
            )
        elif "aggregation" in self.procedures:
            results = results_aggregation
        elif "deliberation" in self.procedures:
            results = results_deliberation
        else:
            return

        # Save results to CSV
        if results is not None:
            results.to_csv(self.filename_csv)

    def get_params(self):
        params = []
        total: int = 0
        if "expert" in self.group_types:
            params = it.chain(params, ["expert"])
            total += 1
        for group_type in self.group_types:
            if (
                "diverse" in group_type
                or "restricted" in group_type
                or "random" in group_type
            ):
                params = it.chain(params, it.repeat(group_type, self.n_samples))
                total += self.n_samples
        return params, total

    def group_simulate(self, composition: str, procedure: str):
        group_params = {
            "sources": copy.deepcopy(self.sources),
            "heuristic_size": self.heuristic_size,
            "size": self.group_size,
        }
        accuracy = None
        precision = None
        diversity = None
        average = None

        if "deliberation" in procedure:
            if composition == "expert":
                team = generate_expert_team(**group_params)
            elif composition == "diverse":
                team = generate_diverse_team(**group_params)
            elif composition == "random":
                team = generate_restricted_team(**group_params)
            elif "restricted" in composition:
                qualified_percentile = float(composition.split("_")[-1])
                team = generate_restricted_team(
                    **group_params, qualifying_percentile=qualified_percentile
                )
            else:
                raise ValueError(f"Unknown group type: {composition}")

            accuracy = team.accuracy_evidence()
            precision = np.nan
            diversity = team.diversity()
            average = team.average()

        elif "aggregation" in procedure:
            if composition == "diverse":
                crowd = generate_random_crowd(**group_params)
            elif composition == "random":
                crowd = generate_random_crowd(**group_params)
            elif "restricted" in composition:
                qualified_percentile = float(composition.split("_")[-1])
                crowd = generate_random_crowd(
                    **group_params, qualifying_percentile=qualified_percentile
                )
            elif composition == "expert":
                raise Warning(
                    "Aggregation procedure not implemented for expert team type. Skipping."
                )
            else:
                raise ValueError(f"Unknown group type: {composition}")

            accuracy, precision = crowd.accuracy_opinion(
                estimate_sample_size=self.estimate_sample_size
            )
            diversity = np.nan
            average = crowd.average()

        heuristic_str = str(self.heuristic_size)  # type: ignore
        if isinstance(self.heuristic_size, list):
            heuristic_str = str(heuristic_str)[1:-1].replace(", ", "-")  # type: ignore

        results_dict = {
            "group_size": self.group_size,
            "n_sources": self.n_sources,
            "heuristic_size": heuristic_str,
            "reliability_mean": self.reliability_distribution[1],
            "reliability_range": self.reliability_distribution[2],
            "n_samples": self.n_samples,
            "group_type": composition,
            "procedure": procedure,
            "accuracy": accuracy,
            "precision": precision,
            "diversity": diversity,
            "average": average,
        }
        return results_dict


if __name__ == "__main__":
    Simulation(n_sources=21, n_samples=2, estimate_sample_size=100).run()
