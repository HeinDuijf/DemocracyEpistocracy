from figures.generate_heatmap import heatmap
from figures.generate_whiskerplot import produce_whiskers_plot
from figures.individual_scores import boxplot_individual_scores

if __name__ == "__main__":
    colors = False
    # heatmap(procedure="deliberation", colors=colors)
    produce_whiskers_plot(
        filename="figures/images/whiskerplot_all",
        n_sources_list=[13, 17],
        rel_mean_list=[0.55, 0.6],
    )
    # produce_whiskers_plot(
    #     n_sources_list=[13],
    #     rel_mean_list=[0.55],
    #     filename="figures/images/whiskerplot_13_55",
    # )
    # boxplot_individual_scores()
