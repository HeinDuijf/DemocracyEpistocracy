import random as rd
from collections import Counter

import numpy as np

import utils.config as cfg
from models.sources import Sources
from models.team import Team
from utils.basic_functions import calculate_accuracy_precision_proportion, powerset


class Crowd(Team):
    """
    A class representing a crowd, which is a team but then optimized for
    large crowds with duplicate heuristics.

    Attributes
    ----------
        members (Counter[Agent]):
            A multiset containing the members of the crowd with counts of how often
            each Agent occurs.
        sources (Sources):
            The sources that the crowd could access.
        size (int):
            The size of the crowd.

    Methods
    -------
        accuracy_opinion:
            Returns the accuracy for the opinion-based dynamics.
        accuracy_evidence:
            Returns the accuracy for the evidence-based dynamics.
        accuracy_bounded:
            Returns the accuracy for the boundedly rational evidence-based dynamics.
    """

    def __init__(self, members: Counter, sources: Sources):
        super().__init__(members, sources)

        self.opinions = Counter()

    def update_opinions(self):
        self.opinions = Counter()
        for agent in self.members:
            agent.update_opinion()
            self.opinions[agent.opinion] += self.members[agent]

    def aggregate(self, return_value: bool = True) -> int | list:
        if self.opinions[cfg.vote_for_positive] > self.opinions[cfg.vote_for_negative]:
            result = [cfg.vote_for_positive]
        elif (
            self.opinions[cfg.vote_for_positive] < self.opinions[cfg.vote_for_negative]
        ):
            result = [cfg.vote_for_negative]
        else:
            result = [cfg.vote_for_positive, cfg.vote_for_negative]

        if return_value:
            return rd.choice(result)
        else:
            return result

    def accuracy_opinion(
        self, estimate_sample_size: int | None = None
    ) -> tuple[float, float | None]:
        # 1. Estimate by sampling if estimate_sample_size is integer
        if isinstance(estimate_sample_size, int):
            outcomes = np.array([], dtype=float)
            for _ in range(estimate_sample_size):
                self.sources.update_valences()
                self.update_opinions()
                result = self.aggregate()
                outcomes = np.append(outcomes, result)
            estimated_accuracy, precision = calculate_accuracy_precision_proportion(
                outcomes
            )
            return estimated_accuracy, precision

        # 2. Else calculate
        sources_relevant = np.unique(
            np.array(
                [source for agent in self.members for source in agent.heuristic]
            ).flatten()
        )
        # sources_relevant = np.unique(sources_relevant.flatten())
        # heuristics = [agent.heuristic for agent in self.members]
        # sources_relevant = np.unique(heuristics.flatten())

        accuracy = 0
        for sources_positive in powerset(sources_relevant):
            for source in self.sources.sources:
                if source in sources_positive:
                    self.sources.set_valence(source, cfg.vote_for_positive)
                else:
                    self.sources.set_valence(source, cfg.vote_for_negative)

            self.update_opinions()
            team_decision = self.aggregate(return_value=False)

            if len(team_decision) == 1 and cfg.vote_for_positive in team_decision:
                probabilities_list = [
                    self.sources.reliabilities[source] for source in sources_positive
                ] + [
                    1 - self.sources.reliabilities[source]
                    for source in sources_relevant
                    if source not in sources_positive
                ]
                probability_subset = np.prod(probabilities_list)
                accuracy += probability_subset
            elif len(team_decision) == 2:
                probabilities_list = [
                    self.sources.reliabilities[source] for source in sources_positive
                ] + [
                    1 - self.sources.reliabilities[source]
                    for source in sources_relevant
                    if source not in sources_positive
                ]
                probability_subset = np.prod(probabilities_list)
                accuracy += probability_subset / 2
        return float(accuracy), None
