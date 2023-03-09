import pandas as pd
import numpy as np

def season_of_date_SH(date):
    year = str(date.year)
    seasons = {'spring': pd.date_range(start=year+'-09-01', end=year+'-11-30'),
               'summer': pd.date_range(start=year+'-12-01', end=year+'-02-28'),
               'autumn': pd.date_range(start=year+'-03-01', end=year+'-05-31')}
    if date in seasons['spring']:
        return 'spring'
    if date in seasons['summer']:
        return 'summer'
    if date in seasons['autumn']:
        return 'autumn'
    else:
        return 'winter'
def season_of_date_NH(date):
    year = str(date.year)
    seasons = {'spring': pd.date_range(start=year+'-03-01', end=year+'-05-31'),
               'summer': pd.date_range(start=year+'-06-01', end=year+'-08-31'),
               'autumn': pd.date_range(start=year+'-09-01', end=year+'-11-30')}
    if date in seasons['spring']:
        return 'spring'
    if date in seasons['summer']:
        return 'summer'
    if date in seasons['autumn']:
        return 'autumn'
    else:
        return 'winter'

def get_seed_harv(data_):
    field_seed_date = {}

    raw_seed_data = data_.seeding_date.values
    raw_harv_data = data_.harvesting_date.values
    raw_field_data = data_.field_shared_name.values
    for id_, name_ in data_.field_shared_name.attrs.items():
        first_indx = np.where(raw_field_data == int(id_))[0][0]
        field_seed_date[name_] = [
            pd.to_datetime(data_.seeding_date.attrs[str(raw_seed_data[first_indx])]),
            pd.to_datetime(data_.harvesting_date.attrs[str(raw_harv_data[first_indx])]),
            ]
    return pd.DataFrame.from_dict(field_seed_date,orient="index", columns=["seeding_date", "harvesting_date"])

def include_season_NH(df):    
    df['season_seed'] = df.seeding_date.map(season_of_date_NH)
    df['season_harv'] = df.harvesting_date.map(season_of_date_NH)

def include_season_SH(df):    
    df['season_seed'] = df.seeding_date.map(season_of_date_SH)
    df['season_harv'] = df.harvesting_date.map(season_of_date_SH)
