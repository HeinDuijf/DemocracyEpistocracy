# Epistemic Democracy and Epistocracy


This repository is associated with a working paper titled ‘Epistemic Democracy and Epistocracy: A Simulation Study’. Here's the abstract: 

> The debate between democracy and epistocracy sits at the core of political epistemology. Epistocrats argue that political decisions should be made by the knowledgeable few, claiming that expertise leads to superior outcomes. Democratic theorists predominantly argue that inclusive participation is superior in promoting a variety of non-epistemic values. In addition, epistemic democratic theorists counter that inclusive participation and the aggregation or exchange of diverse perspectives can outperform expert rule. To evaluate this epistemic tradeoff, this paper uses agent-based modeling to systematically compare institutional arrangements along two dimensions: modes of decision-making (deliberation vs. aggregation) and the composition of the group (expert vs. restricted vs. diverse).

This repository investigates the collective problem-solving capacities of teams in an evidential sources framework. The simulation study focuses on the following arrangements:
1. Deliberation is evidence-based: it is modelled as the exchange of ‘evidences’ and the team’s decision follows the majority evidence. 
    - I consider the following types of teams:
        - Diverse teams selected to optimize diversity. 
        - Expert teams consisting of the best-performing agents.
        - Restricted teams selected to optimize diversity but excluding a proportion of the worst-performing agents. 
2. Aggregation is opinion-based: it is modelled as the sharing of opinions and the crowd’s decision follows the majority opinion.
    - I consider the following types of crowds:
        - Diverse crowds are modelled by maximal inclusivity.
        - Restricted crowds consisting of a subset of the total set of agents that excludes a proportion of worst-performing agents. 
        - Expert teams consisting of a subset of the total set of agents that includes only the proportion of best-performing agents.


To get a feel for the 
agent-based model, see the picture below and the [Jupyter Notebook](/NotebookWalkthrough.ipynb) or the [GitHub page](https://heinduijf.github.io/DiversityAbility/).

[![A picture of an example of a team consisting of randomly selected agents](/www/example_random_team.png "An example of an agent-based model")]()


## 1. Setup
To run the project, you first need to install the required packages
```commandline
pip install -r requirements.txt
```

## 2. Simulation
1. To get a feel for the agent-based model, you can check out this
[Jupyter Notebook](NotebookWalkthrough.ipynb) (or the [GitHub page](https://heinduijf.github.io/DiversityAbility/)), which includes some network 
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

### Illustration of the agent-based model: notebook `NotebookWalkthrough.ipynb` and folder `www` (also see the [GitHub page](https://heinduijf.github.io/DiversityAbility/))
The Jupyter Notebook walks through the stages of the agent-based model `Team` using some network visualizations. Running the notebook will create visualizations in the folder `www`. These can also be viewed on the [GitHub page](https://heinduijf.github.io/DiversityAbility/). 

### Models: folder `models`

- The agent-based model is implemented in the central class `Team`, which is located in `models/team.py`. A `Team` is an *agent-based model* consisting of sources and agents. The central methods `accuracy_opinion` and `accuracy_evidence` compute the accuracy of the team for the opinion-based and evidence-based dynamics, respectively.

- The class `Team` relies on the classes `Sources` and `Agent` implementing the sources (and their reliability) ant the agents (and their heuristics), which are located `models/sources.py` and `models/agent.py`, respectively. 

- The central methods for generating the three types of teams can be found in `models/generate_teams.py`: `generate_expert_team`, `generate_diverse_team`, and `generate_restricted_team`.

<!-- ### Data analysis: folder `data_analysis` and notebook `DataAnalysis.ipynb`
The notebook contains statistical results and heatmaps illustrating the trade-off between expertise and diversity. It relies on the scripts for the Wilcoxon test, which are located in `data_analysis/statistics.py`.  -->

### Simulations: `simulation.py` and `grid_simulation.py`
The class `Simulation` and method `Simulation.run()` is located in `simulation.py`, the method produces a csv file (by default, in the folder `data`). The method `Simulation.run()` runs a simulation for a particular parameter setting and produces results that can give insight into whether diversity trumps ability for that parameter setting. 

The class `GridSimulation` and method `GridSimulation.run()` is located in `grid_simulation.py`. The method runs simulations (by invoking the method `Simulation.run()`) for each parameter setting in a grid. 

### Figures: `figures.py`
The figures in the paper can be reproduced by running `figures.py`, but it requires the necessary simulation data in `data`. This will create the figures in the folder `figures/images` by running scripts in the folder `figures`, especially the `heatmap` script located in `figures/generate_heatmap.py`.

<!-- ### Robustness analysis: `Robustness.ipynb`
The notebook contains various robustness checks for the main simulation results. 

### Analytical approaches: `Analytical.ipynb`
The notebook considers the question of whether the diversity-expertise tradeoff (as modelled by the evidential sources model) can be studied analytically, using approaches from the voting literature. To investigate this, it covers: (1) A lower bound in terms of number of sources and their mean reliability; (2) The Cantelli lower bound (in terms of $\mu$ and $\sigma$); and (3) Normal approximation.  -->

## 5. Computational limitations
* This repository is not optimized for computational speed, but for findability, accessibility, interoperability, and reusability ([FAIR](https://www.uu.nl/en/research/research-data-management/guides/how-to-make-your-data-fair)).

## 6. Licence and citation
This repository accompanies an academic paper (in progress). Please cite this repository as follows:
- Duijf, H. (2026). _Democratic and epistocratic forms of aggregation and deliberation in an evidential sources framework_. 

Released under the [MIT licence](LICENCE.md).
