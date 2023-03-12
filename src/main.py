import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from src.coverage_analysis.dataset_coverage_analysis import analyze_dataset


if __name__ == "__main__":
    dataset_structure_path = '../coverage/landcovernet_eu/landcovernet_structure_europe.yaml'

    strategy= 'by_classes' #'by_classes' #'by_clouds'
    idx_targets = [4,5] #[4,5] #[8,9,3]
    min_spatial_coverage=70
    min_temporal_coverage=70      
    output_dir = "../coverage/landcovernet_eu/"
    num_process=-1
    results = analyze_dataset(dataset_structure_path = dataset_structure_path, 
                              idx_targets = idx_targets, 
                              strategy = strategy, 
                              min_spatial_coverage = min_spatial_coverage, 
                              min_temporal_coverage = min_temporal_coverage,
                              output_dir=output_dir,
                              num_process=num_process
                              )