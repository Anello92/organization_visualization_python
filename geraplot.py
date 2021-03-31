import matplotlib as mpl
import matplotlib.pyplot as plt

import radar

import geradados


colors = [color['color'] for color in list(mpl.rcParams['axes.prop_cycle'])]

def hide_axes(axes):
    axes.set_frame_on(False)
    [n.set_visible(False) for n in axes.get_xticklabels() + axes.get_yticklabels()]
    [n.set_visible(False) for n in axes.get_xticklines() + axes.get_yticklines()]


def make_autos_radar_plot(
    figure, gs = None, pddata = None, title_axes = None, legend_axes = None, inner_axes = None, geometry = None, rotate = True):
    radar_colors = [1, 2, 0]
    min_data = pddata.groupby("make", sort = True).min()
    max_data = pddata.groupby("make", sort = True).max()
    mean_data = pddata.groupby("make", sort = True).mean()
    projection = radar.RadarAxes(spoke_count = len(mean_data.columns))
    if geometry:
        (row_num, col_num) = geometry
    else:
        (row_num, col_num) = gs.get_geometry()
    if not inner_axes:
        subplots = [x for x in gs]
        inner_axes = []
        for (i, m) in enumerate(subplots[col_num:]):
            if i % col_num != 0:
                inner_axes.append(plt.subplot(m, projection = projection))
    if not title_axes:
        title_axes = figure.add_subplot(gs[0, :])
    if legend_axes is None:
        legend_axes = figure.add_subplot(gs[0:, 0])
    if legend_axes != False:
        max_patch = mpl.patches.Patch(color = colors[radar_colors[0]], alpha = 0.7, label = "Max")
        mean_patch = mpl.patches.Patch(color = colors[radar_colors[1]], alpha = 0.7, label = "Mean")
        min_patch = mpl.patches.Patch(color = colors[radar_colors[2]], alpha = 0.7, label = "Min")
        legend_axes.legend(handles = [max_patch, mean_patch, min_patch], loc = 10)
        hide_axes(legend_axes)
    title_axes.set_title("Radar Plot com 7 Dimensões\nPara 12 Fabricantes", fontsize = 16)
    hide_axes(title_axes)
    for i, make in enumerate(geradados.get_make_names(pddata)):
        axes = inner_axes[i]
        axes.set_title(
            make.title(), size = 'large', position = (0.5, 1.2), horizontalalignment = 'center', verticalalignment = 'center')
        for (color, alpha, data) in zip(radar_colors,
                                        [0.2, 0.3, 0.4],
                                        [max_data, mean_data, min_data]):
            axes.fill(axes.radar_theta, data.loc[make], color = colors[color], alpha = alpha)
            axes.plot(axes.radar_theta, data.loc[make], color = colors[color])
        axes.set_varlabels([x.replace(" ", "\n") for x in mean_data.columns])
        axes.set_yticklabels([])
    if gs:
        gs.tight_layout(figure)
    return [title_axes, legend_axes, inner_axes]


def make_empty_plot(figure, gs):
    axes = figure.add_subplot(gs[0, 0])
    axes.set_title("Empty Plot", fontsize=20)
    gs.tight_layout(figure)
    return axes


def make_autos_mpg_plot(figure, gs = None, pddata = None, axes = None):
    if not axes:
        axes = figure.add_subplot(gs[0, 0])
    data = geradados.get_numeric_data(pddata)
    axes.set_title("Ranges of Cidades e Velocidade", fontsize = 20)
    axes.scatter(data["make"], data["highway mpg"], c = colors[3], s = 500, alpha = 0.4)
    axes.scatter(data["make"], data["city mpg"], c = colors[0], s = 500, alpha = 0.4)
    axes.set_xticks(range(0, 13))
    axes.set_xticklabels(geradados.get_make_labels(pddata))
    axes.set_xlabel("Make", fontsize = 16)
    axes.set_ylabel("MPG", fontsize = 16)
    city_patch = mpl.patches.Patch(color = colors[0], alpha = 0.7, label = "City")
    highway_patch = mpl.patches.Patch(color=colors[3], alpha=0.7, label = "Highway")
    axes.legend(handles=[city_patch, highway_patch], loc = 2)
    if gs:
        gs.tight_layout(figure)
    return axes


def make_autos_price_plot(figure, gs = None, pddata = None, axes = None):
    if not axes:
        axes = figure.add_subplot(gs[0, 0])
    min_data = pddata.groupby("make", sort=True)["price"].min()
    max_data = pddata.groupby("make", sort=True)["price"].max()
    mean_data = pddata.groupby("make", sort=True)["price"].mean()
    make_ids = geradados.get_make_ids(pddata)
    axes.set_title("Auto Price Ranges", fontsize=20)
    axes.plot(make_ids, min_data, c=colors[2], linewidth=4, alpha=0.7)
    axes.plot(make_ids, mean_data, c=colors[3], linewidth=4, alpha=0.7)
    axes.plot(make_ids, max_data, c=colors[4], linewidth=4, alpha=0.7)
    axes.set_xticks(range(-1, 13))
    axes.set_xticklabels([" "] + geradados.get_make_labels(pddata))
    axes.set_xlabel("Make", fontsize=16)
    axes.set_ylabel("Price", fontsize=16)
    high_patch = mpl.patches.Patch(color=colors[4], alpha=0.7, label="High")
    mean_patch = mpl.patches.Patch(color=colors[3], alpha=0.7, label="Mean")
    low_patch = mpl.patches.Patch(color=colors[2], alpha=0.7, label="Low")
    axes.legend(handles=[high_patch, mean_patch, low_patch], loc=2)
    if gs:
        gs.tight_layout(figure)
    return axes


def make_autos_riskiness_plot(
    figure, gs=None, pddata=None, axes=None,legend=True, labels=True):
    if not axes:
        axes = figure.add_subplot(gs[0, 0])
    risk_mins = pddata.groupby("make")["riskiness"].min().values
    risk_means = pddata.groupby("make")["riskiness"].mean().values
    risk_maxs = pddata.groupby("make")["riskiness"].max().values
    make_ids = geradados.get_make_ids(pddata)
    min_color = colors[0]
    mean_color = colors[3]
    max_color = colors[2]
    axes.set_title("Inverse Risk", fontsize=14)
    mins_bar = axes.bar(make_ids, risk_mins, width=0.5, align="center",
                        color=min_color, alpha=0.7)
    means_bar = axes.bar(make_ids, risk_means, width=0.5, align="center",
                         bottom=risk_mins, color=mean_color, alpha=0.7)
    maxs_bar = axes.bar(make_ids, risk_maxs, width=0.5, align="center",
                        bottom=risk_means + risk_mins, color=max_color, alpha=0.7)
    if labels:
        axes.set_xticks(range(0, 13))
        axes.set_xticklabels(geradados.get_make_labels(pddata))
        axes.set_xlabel("Make", fontsize=12)
        axes.set_ylabel("Inverse Risk", fontsize=12)
    else:
        axes.set_xticklabels([])
        axes.set_yticklabels([])
    if legend:
        axes.legend([mins_bar, means_bar, maxs_bar], ["Min", "Mean", "Max"], loc=2)
    if gs:
        gs.tight_layout(figure)
    return axes


def make_autos_losses_plot(
    figure, gs=None, pddata=None, axes=None, legend=True, labels=True):
    if not axes:
        axes = figure.add_subplot(gs[0, 0])
    loss_mins = pddata.groupby("make")["losses"].min().values
    loss_means = pddata.groupby("make")["losses"].mean().values
    loss_maxs = pddata.groupby("make")["losses"].max().values
    make_ids = geradados.get_make_ids(pddata)
    min_color = colors[0]
    mean_color = colors[3]
    max_color = colors[2]
    axes.set_title("Inverse Losses", fontsize=14)
    mins_bar = axes.bar(make_ids, loss_mins, width=0.5, align="center",
                        color=min_color, alpha=0.7)
    means_bar = axes.bar(make_ids, loss_means, width=0.5, align="center",
                         bottom=loss_mins, color=mean_color, alpha=0.7)
    maxs_bar = axes.bar(make_ids, loss_maxs, width=0.5, align="center",
                        bottom=loss_means + loss_mins, color=max_color, alpha=0.7)
    if labels:
        axes.set_xticks(range(0, 13))
        axes.set_xticklabels(geradados.get_make_labels(pddata))
        axes.set_xlabel("Make", fontsize=12)
        axes.set_ylabel("Inverse Losses", fontsize=12)
    else:
        axes.set_xticklabels([])
        axes.set_yticklabels([])
    if legend:
        axes.legend([mins_bar, means_bar, maxs_bar], ["Min", "Mean", "Max"], loc=2)
    if gs:
        gs.tight_layout(figure)
    return axes


def make_autos_loss_and_risk_plot(
    figure, gs=None, pddata=None, axes=None, x_label=True, rotate_ticks=False):
    if not axes:
        axes = figure.add_subplot(gs[0, 0])
    if rotate_ticks:
        plt.xticks(rotation=70)
    risk_mins = pddata.groupby("make")["riskiness"].min().values
    risk_means = pddata.groupby("make")["riskiness"].mean().values
    risk_maxs = pddata.groupby("make")["riskiness"].max().values
    loss_mins = pddata.groupby("make")["losses"].min().values
    loss_means = pddata.groupby("make")["losses"].mean().values
    loss_maxs = pddata.groupby("make")["losses"].max().values
    mins = risk_mins + loss_mins
    means = risk_means + loss_means
    maxs = risk_maxs + loss_maxs
    make_ids = geradados.get_make_ids(pddata)
    min_color = colors[0]
    mean_color = colors[3]
    max_color = colors[2]
    axes.set_title(("Combined Losses and Riskiness Data\n"
                    "(Inverted, Normalized)"),
                   fontsize=16)
    mins_bar = axes.bar(make_ids, mins, align="center", color=min_color,
                        alpha=0.7)
    means_bar = axes.bar(make_ids, means, align="center", bottom=mins,
                         color=mean_color, alpha=0.7)
    maxs_bar = axes.bar(make_ids, maxs, align="center", bottom=means + mins,
                        color=max_color, alpha=0.7)
    axes.set_xticks(range(0, 13))
    axes.set_xticklabels(geradados.get_make_labels(pddata))
    if x_label:
        axes.set_xlabel("Make", fontsize = 12)
    axes.set_ylabel("Risco", fontsize = 12)
    axes.legend([mins_bar, means_bar, maxs_bar], ["Min", "Mean", "Max"], loc = 2)
    if gs:
        gs.tight_layout(figure)
    return axes

    
