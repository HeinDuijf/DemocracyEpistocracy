from figures.comparison_weighted_procedure import (
    line_plot_comparison_weighted_procedure,
)
from figures.generate_combined_lineplot import combined_lineplot
from figures.generate_heatmap import heatmap
from figures.generate_weights_lineplot import weights_lineplot
from figures.individual_scores import boxplot_individual_scores

if __name__ == "__main__":
    colors = False

    boxplot_individual_scores()
    heatmap(
        procedure="deliberation",
        colors=colors,
        rel_mean_max=0.60,
        filename="figures/images/heatmap_deliberation",
    )
    combined_lineplot(
        n_sources_list=[13, 17],
        rel_mean_max=0.60,
        filename="figures/images/lineplot_combined",
    )
    combined_lineplot(
        show_aggregation=False,
        n_sources_list=[13, 17],
        rel_mean_max=0.60,
        filename="figures/images/lineplot_combined_without_aggregation",
    )
    weights_lineplot(
        n_sources=13,
        filename="figures/images/weights",
    )
    line_plot_comparison_weighted_procedure(
        rel_mean_max=0.6,
        show_progress=True,
        filename="figures/images/accuracy_difference_vs_weights",
    )
