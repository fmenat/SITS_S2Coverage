import pandas as pd
def dict_to_df(dict_:dict):
    '''Converts dictionary to dataframe
    
    '''
    #save_json(output_report_dir, report_dict)
    df = pd.DataFrame.from_dict(dict_, orient='index')
    df.index.name = 'filename'
    return df