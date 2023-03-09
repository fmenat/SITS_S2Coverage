import os
from tqdm import tqdm
from src.coverage_analysis.patch_coverage_analysis import CoverageAnalysis
from src.utils.dict_to_df import dict_to_df

def analyse_dataset(input_dir:str, idx_targets:list, boundary_mask=None,
                    strategy:str='by_clouds',min_spatial_coverage:int=50, min_temporal_coverage:int=50):
    output_report_path = os.path.join(input_dir, 'assesment_report_{}_{}.csv'.format(min_spatial_coverage,min_temporal_coverage))
    assesment_accumulated = {}
    patches = [p for p in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir,p))]
    for patch in tqdm(patches):
        #print(patch)
        boundary_mask = None
        #boundary_mask = os.path.join(input_dir,patch,'yield_masks','mean_scaled_yield_masked_regional_statistical_outlier.tif')
        timeseries_dir = os.path.join(input_dir,patch,'scl_masks')
        if os.path.isdir(timeseries_dir):
            CA =  CoverageAnalysis(timeseries_dir, idx_targets, boundary_mask,
                                        strategy,min_spatial_coverage, min_temporal_coverage)
            assesment = CA.temporal_spatial_coverage()
            assesment_accumulated[patch]=assesment
    result = dict_to_df(assesment_accumulated)
    result.to_csv(output_report_path)
    print(">Analysis finalized and stored in: ",output_report_path)
    return result