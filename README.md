# Epistemic Democracy and Epistocracy


This repository is associated with a working paper titled ‘Epistemic Democracy and Epistocracy: A Simulation Study’ ([PhilSci-Archive](https://philsci-archive.pitt.edu/id/eprint/30758)). Here's the abstract: 

> The debate between democracy and epistocracy sits at the core of political epistemology. Epistemic democrats commonly argue that democratic procedures—in particular, voting procedures with universal suffrage and deliberative procedures with diverse groups—outperform expert rule because of inclusive participation and the aggregation or exchange of diverse perspectives. In contrast, epistocrats argue that political decisions should be made by the knowledgeable few, claiming that expertise leads to superior outcomes, especially in light of citizens’ staggering lack of political knowledge. To evaluate the potential tradeoffs, this paper uses agent-based modelling to systematically compare institutional arrangements along two dimensions: the type of procedure (deliberation or aggregation) and the enfranchisement restrictions, if any (expert only, competence restriction, or inclusive). I argue that this formal study improves our understanding of the complex interactions between institutional design, participant selection, and epistemic performance.

This repository investigates the collective problem-solving capacities of teams in an evidential sources framework. The simulation study focuses on the following arrangements:
1. Deliberation is evidence-based: it is modelled as the exchange of ‘evidences’ and the team’s decision follows the majority evidence. 
    - I consider the following types of teams:
        - Diverse teams selected to optimize diversity. 
        - Expert teams consisting of the best-performing agents.
        - Restricted teams selected to optimize diversity but excluding a proportion of the worst-performing agents. 
2. Aggregation is opinion-based: it is modelled as the sharing of opinions and the crowd’s decision follows the majority opinion.
    - Crowds are sampled with replacement from a set of admissible heuristics; I consider three cases: 
        - Democratic aggregation places no admissibility constraints on the heuristics.
        - Permissive and expert aggregation involve epistemic thresholds: _permissive aggregation includes_ all but a small proportion of worst-performing individuals, while _expert aggregation excludes_ all but a small proportion of best-performing individuals. 


To get a feel for the 
agent-based model, see the picture below and the [Jupyter Notebook](/NotebookWalkthrough.ipynb) or the [GitHub page](https://heinduijf.github.io/DemocracyEpistocracy/).

[![A picture of an example of a team consisting of randomly selected agents](/www/example_random_team.png "An example of an agent-based model")]()


## 1. Setup
To run the project, you first need to install the required packages using pip
```commandline
pip install -r requirements.txt
```

or using Anaconda to create and activate an environment called `work`:

```commandline
conda env create -f environment.yml
conda activate work
```

## 2. Simulation
1. To get a feel for the agent-based model, you can check out this
[Jupyter Notebook](NotebookWalkthrough.ipynb) (or the [GitHub page](https://heinduijf.github.io/DemocracyEpistocracy/)), which includes some network 
visualizations by running
```commandline
jupyter lab NotebookWalkthrough.ipynb
```
Running the cells in the notebook will create several html files in the folder `www` with 
visualizations of agent-based models.

2. To run the simulations and generate the data, run the script
```commandline
python main.py
```
which will create several csv files in the folder `data`.

<!-- 3. To check out the data analysis, you can run this [Jupyter Notebook](DataAnalysis.ipynb) by running
```commandline
jupyter lab DataAnalysis.ipynb
``` -->

## 3. Organization of the repository

### Illustration of the agent-based model: notebook `NotebookWalkthrough.ipynb` and folder `www` (also see the [GitHub page](https://heinduijf.github.io/DemocracyEpistocracy/))
The Jupyter Notebook walks through the stages of the agent-based model using some network visualizations. Running the notebook will create visualizations in the folder `www`. These can also be viewed on the [GitHub page](https://heinduijf.github.io/DemocracyEpistocracy/). 

### Models: folder `models`

- The agent-based model is implemented in the central class `Team`, which is located in `models/team.py`. A `Team` is an *agent-based model* consisting of sources and agents. The central methods `accuracy_opinion` and `accuracy_evidence` compute the accuracy of the team for aggregation and deliberation, respectively.

- The agent-based model for aggregative crowds is implemented in the class `Crowd`, which is located in `models/crowd.py`, which inherits from `Team`. A `Crowd` is more optimized for the cases where the group contains agents with identical heuristics. 

- The classes `Team` and `Crowd` rely on the classes `Sources` and `Agent` implementing the sources (and their reliability) ant the agents (and their heuristics), which are located `models/sources.py` and `models/agent.py`, respectively. 

- The central methods for generating the three types of teams can be found in `models/generate_teams.py`: `generate_expert_team`, `generate_diverse_team`, and `generate_restricted_team`.

<!-- ### Data analysis: folder `data_analysis` and notebook `DataAnalysis.ipynb`
The notebook contains statistical results and heatmaps illustrating the trade-off between expertise and diversity. It relies on the scripts for the Wilcoxon test, which are located in `data_analysis/statistics.py`.  -->

### Simulations: `simulation.py` and `grid_simulation.py`
The class `Simulation` and method `Simulation.run()` is located in `simulation.py`, the method produces a csv file (by default, in the folder `data`). The method `Simulation.run()` runs a simulation for a particular parameter setting and produces results that can give insight into whether diversity trumps ability for that parameter setting. 

The class `GridSimulation` and method `GridSimulation.run()` is located in `grid_simulation.py`. The method runs simulations (by invoking the method `Simulation.run()`) for each parameter setting in a grid. 

### Figures: `figures.py`
The figures in the paper can be reproduced by running `figures.py`. This will create the figures in the folder `figures/images` by running scripts in the folder `figures`, but some of these require the necessary simulation data in `data`.

<!-- ### Robustness analysis: `Robustness.ipynb`
The notebook contains various robustness checks for the main simulation results. 

### Analytical approaches: `Analytical.ipynb`
The notebook considers the question of whether the diversity-expertise tradeoff (as modelled by the evidential sources model) can be studied analytically, using approaches from the voting literature. To investigate this, it covers: (1) A lower bound in terms of number of sources and their mean reliability; (2) The Cantelli lower bound (in terms of $\mu$ and $\sigma$); and (3) Normal approximation.  -->

## 5. Computational limitations
This repository is not optimized for computational speed, but for findability, accessibility, interoperability, and reusability ([FAIR](https://www.uu.nl/en/research/research-data-management/guides/how-to-make-your-data-fair)).

## 6. Licence and citation
This repository accompanies an academic paper (draft available on [PhilSci-Archive](https://philsci-archive.pitt.edu/id/eprint/30758)). Please cite this repository as follows:
- Duijf, H. (2026). _Democratic and epistocratic forms of aggregation and deliberation in an evidential sources framework_. 

Released under the [MIT licence](LICENCE.md).
