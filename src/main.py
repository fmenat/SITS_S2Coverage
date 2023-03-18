import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from src.coverage_analysis.dataset_coverage_analysis import analyze_dataset
from src.coverage_analysis.SCL import IND_ALL_,IND_CLOUDS_, remove_labels


if __name__ == "__main__":
    #dataset_structure_path = '../coverage/landcovernet_eu/landcovernet_structure_europe.yaml'
    dataset_structure_path = '../coverage/YC/MX_First.yaml'
    #dataset_structure_path = '../coverage/ai4eo/test.yaml'#/test.yaml' #/train.yaml
    idx_targets = remove_labels(IND_ALL_, IND_CLOUDS_) #index to be selected (all except 3, 8 and 9)
    min_spatial_coverage=70
    min_temporal_coverage=70      
    output_dir = "../coverage/YC"
    num_process=-1
    results = analyze_dataset(dataset_structure_path = dataset_structure_path, 
                                idx_targets = idx_targets, 
                                min_spatial_coverage = min_spatial_coverage, 
                                min_temporal_coverage = min_temporal_coverage,
                                output_dir=output_dir,
                                num_process=num_process
                                )