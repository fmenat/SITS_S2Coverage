
import pandas as pd
from IPython.display import display

from src.utils.plots import plot_boxplots

def build_attached_dataframe(df_source, df_target):
    return  pd.merge(df_target, df_source, left_index=True, right_index=True, how='right')

def add_topk_column(df_data, k=5, column="temporal_coverage"):
    limit_ = df_data[column].sort_values()[k]
    print(f"Limit {column} is {limit_}")
    df_data[f"assesment_top{k}"] = (df_data[column] <= limit_).apply(lambda x: "low" if x else "high")

def plot_col_categorization(df_quality, df_metrics, metrics_cols=["MCC", "ACC"], col="assesment_temporal", division=None):
    report_all = build_attached_dataframe(df_metrics, df_quality)

    plot_boxplots(report_all, cols= metrics_cols, group_by = col, division=division)
    display(report_all.groupby([col])[metrics_cols].describe())
    return report_all