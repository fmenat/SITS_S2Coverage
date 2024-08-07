import os
from tqdm import tqdm
from datetime import datetime
from src.coverage_analysis.patch_coverage_analysis import CoverageAnalysis
from src.utils.dict_to_df import dict_to_df
from src.utils.read_utils import read_yaml
from src.multiprocess.multiprocess import mp_proxy


def analyze_patch(
        patch_name:str, 
        idx_targets:list, 
        min_spatial_coverage:int, 
        min_temporal_coverage:int,
        dataset_structure: dict,
        ):
    patch_structure = dataset_structure[patch_name]
    print("Starting to execute patch", patch_name)
    boundary_mask = None
    scl_mask_paths = patch_structure['scl_mask_paths']
    boundary_paths = patch_structure['boundary_paths']
    CA =  CoverageAnalysis(scl_mask_paths, idx_targets, boundary_paths,
                                min_spatial_coverage, min_temporal_coverage)
    assesment = CA.temporal_spatial_coverage()

    return {"assesment": assesment, "patch_name": patch_name}


def analyze_dataset(
        dataset_structure_path:str, 
        idx_targets:list, 
        min_spatial_coverage:int=50, 
        min_temporal_coverage:int=50,
        output_dir: str = "",
        num_process=1,
        include_date: bool = True,
        ):
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
    
    #configure multiprocessing
    mp_inst = mp_proxy(
        iterable=dataset_structure,
        func=analyze_patch,
        static_func_kwargs={
            'idx_targets': idx_targets,
            "min_spatial_coverage": min_spatial_coverage,
            "min_temporal_coverage": min_temporal_coverage,
            "dataset_structure": dataset_structure
            },
        map_type="imap",
        context="fork", #spawn, fork
        processes=num_process,
        chunksize=1,
        )
    
    #start multiprocessing
    print(f"Starting execution with the following configuration idx_targets={idx_targets}, min_spatial_coverage={min_spatial_coverage}, {min_temporal_coverage}=min_temporal_coverage")
    assesment_accumulated = {}
    for patch in tqdm(mp_inst, total=len(dataset_structure)):
        assesment_accumulated[patch["patch_name"]] = patch["assesment"]
    result = dict_to_df(assesment_accumulated)

    #save results
    if output_dir == "":
        output_dir = '../coverage/'
    now = str(int(datetime.now().strftime("%Y%m%d%H%M%S")))
    target_str = "".join([f"{v:02d}" for v in idx_targets])
    if include_date:
        output_report_path = os.path.join(output_dir, 'assesment_spat_{}_temp_{}_sel_{}_{}.csv'.format(min_spatial_coverage,min_temporal_coverage,target_str,now))
    else:
        output_report_path = os.path.join(output_dir, 'assesment_spat_{}_temp_{}_sel_{}.csv'.format(min_spatial_coverage,min_temporal_coverage,target_str))
    result.to_csv(output_report_path)

    print(f">Analysis finished and stored in {output_report_path}")
    return result