from figures.generate_heatmap import heatmap
from figures.individual_scores import boxplot_individual_scores

if __name__ == "__main__":
    colors = True
    heatmap(outcome="accuracy_evidence", colors=colors)
    boxplot_individual_scores()
