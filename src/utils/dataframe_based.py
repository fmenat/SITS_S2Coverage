import pandas as pd
from itertools import islice, repeat, chain

def select_metrics(df: pd.DataFrame, metric_names: list):
    level_columns = len(df.columns.names)
    metric_cols = []
    for col in df.columns:
        if level_columns == 1:
            if  any([m in col for m in metric_names]):
                metric_cols.append(col)
        else:
            if  any([m in col[-1] for m in metric_names]) and col[0] != "METADATA":
                metric_cols.append(col)
    return df[metric_cols]


def filter_rows_inside_dic(dataframe_p_method:dict, row_index:str):
    new_data = {}
    for method in dataframe_p_method:
        new_data[(row_index,) +(method,)] = dataframe_p_method[method].loc[row_index]
    return pd.DataFrame(new_data).T
    

def filter_df_per_cols(df, query_cols, lowercase_search=True):
    #query cols ideally should be all lower-case, since the search is performed on a lower-case dataframe
    new_df = df.copy()
    for col in query_cols:
        if col in df:
            if lowercase_search:
                mask_ = new_df[col].apply(lambda x: x.lower()).isin(query_cols[col])
            else:
                mask_ = new_df[col].isin(query_cols[col])
            new_df = new_df[mask_]
    return new_df

def pad(x, n=0, pad_v=0):
    padv = repeat(pad_v)
    if n==0:
        n = max(map(len, x))
    return [list(islice(chain(row,padv), n)) for row in x]