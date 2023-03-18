import os
from datetime import datetime
from src.utils.read_utils import read_json


#TODO, make it flexible to work with multiple date format, 
#or fix it to a common one (would mean, people need to change file names)

def extract_date_from_filename(filename:str, date_format:str='%Y%m%d'):
    '''Deliveres date from path/filename
    
    '''
    return datetime.strptime(filename.split('_')[3][:-4], date_format).date()

def get_dates(path:str):
    '''Delivers seeding and harvesting dates.
    Searches in field path for metadata-.json file and gets dates.

    Args:
        path (str): e.g. field path 
    
    Returns:
        seeding (datetime): seeding date
        harvesting (datetime): harvesting date
    '''
    meta_file = [i for i in os.listdir(path) if i.endswith('json')][0]
    meta = read_json(os.path.join(path,meta_file))
    seeding = _str_to_datetime(meta['seeding_date'])
    harvesting = _str_to_datetime(meta['harvesting_date'])
    return seeding, harvesting

def _str_to_datetime(string:str,date_format:str='%Y%m%d'):
    '''Bring date from metadata to same format as in SCL masks file names.

    '''
    day,month,year = string.split('.')
    full_date = year+month+day
    return datetime.strptime(full_date, date_format).date()