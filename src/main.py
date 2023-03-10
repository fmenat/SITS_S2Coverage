import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from src.coverage_analysis.dataset_coverage_analysis import analyse_dataset


if __name__ == "__main__":
    dataset_structure_path = '/ds/yieldcon/home/csanchez/projects/SITS_S2Coverage/results/landcovernet_dataset_structure.yml'
    strategy= 'by_clouds' #'by_classes' #'by_clouds'
    idx_targets = [8,9,3] #[4,5] #[8,9,3]
    min_spatial_coverage=50
    min_temporal_coverage=50      
    results = analyse_dataset(dataset_structure_path = dataset_structure_path, 
                              idx_targets = idx_targets, 
                              strategy = strategy, 
                              min_spatial_coverage = min_spatial_coverage, 
                              min_temporal_coverage = min_temporal_coverage)