import os
from tqdm import tqdm
from datetime import datetime
from src.coverage_analysis.patch_coverage_analysis import CoverageAnalysis
from src.utils.dict_to_df import dict_to_df
from src.utils.read_utils import read_yaml

def analyse_dataset(dataset_structure_path:str, idx_targets:list, strategy:str='by_clouds',
                    min_spatial_coverage:int=50, min_temporal_coverage:int=50):
    """
    dataset_structure (str): path to yaml file dictionary containing conventional of dataset:
                                            dataset_structure = {
                                                                Patch_Name:
                                                                            {
                                                                            scl_mask_paths: [list_of_scl_masks_paths_as_per_timeserie]
                                                                            boundary_paths: [list_of_boundary_paths_as_per_timeserie]
                                                                            }
                                                                }
    """
    dataset_structure = read_yaml(dataset_structure_path)
    now = str(int(datetime.now().strftime("%Y%m%d%H%M%S")))
    output_report_path = os.path.join('../results', 'assesment_{}_spatial_{}_temporal_{}.csv'.format(min_spatial_coverage,min_temporal_coverage,now))
    assesment_accumulated = {}
    #patches = [p for p in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir,p))]
    for patch in tqdm(dataset_structure.keys()):
        print(patch)
        #print(patch)
        boundary_mask = None
        #boundary_mask = os.path.join(input_dir,patch,'yield_masks','mean_scaled_yield_masked_regional_statistical_outlier.tif')
        #timeseries_dir = os.path.join(input_dir,patch,'scl_masks')
        scl_mask_paths = dataset_structure[patch]['scl_mask_paths']
        boundary_paths = dataset_structure[patch]['boundary_paths']
        CA =  CoverageAnalysis(scl_mask_paths, idx_targets, boundary_paths,
                                    strategy,min_spatial_coverage, min_temporal_coverage)
        assesment = CA.temporal_spatial_coverage()
        assesment_accumulated[patch]=assesment
    result = dict_to_df(assesment_accumulated)
    result.to_csv(output_report_path)
    print(">Analysis finalized and stored in: ",output_report_path)
    return result