import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

def plot_coverage_perc(df_data, col="avg_spatial_coverage", xticks_included=True):
    df_data = df_data.sort_values(by=col)
    stats = df_data.describe()
    lower_limit = (stats.loc["25%"] - 1.5*(stats.loc["75%"] - stats.loc["25%"]))

    fig, ax = plt.subplots(1,3, squeeze = False, figsize=(25,5),gridspec_kw={'width_ratios': [1, 1, 7]} )
    indexs_ = df_data.index
    ax[0,0].hist(df_data[col], bins=15, orientation="horizontal", alpha=0.5)
    ax[0,0].set_xlabel("number of images")
    ax[0,0].set_ylabel(f"percentage of {col}") 
    ax[0,0].axhline(lower_limit[col])
    ax[0,0].set_ylim(0,100)
    ax[0,1].boxplot(df_data[col])
    ax[0,1].axhline(lower_limit[col], color="r")
    ax[0,1].set_ylim(0,100)
    ax[0,2].plot(df_data.index, df_data[col], marker="o")
    ax[0,2].axhline(lower_limit[col], color="r")
    if xticks_included:
        ax[0,2].set_xticks(indexs_)
        ax[0,2].set_xticklabels(indexs_)
        plt.setp(ax[0,2].get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")
    ax[0,2].set_ylim(0,100)
    ax[0,2].set_xlabel("images")
    plt.show()

    return lower_limit


def plot_boxplots(report_all, cols, group_by, x_label = "", title="", division=None):
    fig, ax = plt.subplots(1, len(cols), squeeze=False, figsize=(17,6))
    for i,col in enumerate(cols):
        bp = sns.boxplot(data=report_all, x=group_by, y=col, hue=division, ax=ax[0,i])
        if division is None:
            sns.stripplot(data=report_all, x=group_by, y=col, size=7, color="red", linewidth=0, ax=ax[0,i], alpha=0.5)
        if x_label != "":
            ax[0,i].set_xlabel(x_label)
        if title != "":
            ax[0,i].set_title(title)
        ax[0,i].set_ylim(0.6,1.05)
    plt.show()