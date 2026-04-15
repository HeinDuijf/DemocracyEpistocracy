import numpy as np

from grid_simulation import GridSimulation

if __name__ == "__main__":
    rels = [("equi", rel_mean, 0.2) for rel_mean in [0.55, 0.6, 0.65]]

    # Deliberation
    team_types = ["expert", "diverse"]
    GridSimulation(
        outcomes=["evidence"],
        team_types=team_types,
        n_sources_list=[13, 17],
        reliability_distribution_list=rels,
        heuristic_size=5,
        team_size=9,
        n_samples=1,
    ).run()

    # Aggregation
    team_types = ["diverse"] + [
        f"restricted_{percentile}" for percentile in np.arange(10, 91, 10, dtype=int)
    ]

    GridSimulation(
        outcomes=["opinion"],
        team_types=team_types,
        n_sources_list=[13, 17],
        reliability_distribution_list=rels,
        heuristic_size=5,
        team_size=1_001,
        n_samples=1_000,
    ).run()
