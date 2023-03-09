import os
from coverage_analysis.dataset_coverage_analysis import analyse_dataset


if __name__ == "__main__":
    #input_dir = '/ds/yieldcon/home/csanchez/data/cloud_analysis/YC/' #TEST CODE
    #input_dir = '/ds/yieldcon/home/csanchez/data/cloud_analysis/Enhanced4Agri/' #TEST CODE
    input_dir = '/ds/images/AI4EO/EnhancedS2Agriculture/preprocessed/train'
    ##por clase 4 y5
    ##incluyendo 3, cuando 8y9
    #input_dir = '/ds/yieldcon/yieldData/VI-delivery/Argentina/MX_First'
    boundary_mask=None
    strategy= 'by_clouds' #'by_classes' #'by_clouds'
    idx_targets = [8,9,3] #[4,5] #[8,9,3]
    min_spatial_coverage=50
    min_temporal_coverage=50      
    results = analyse_dataset(input_dir = input_dir, idx_targets = idx_targets, boundary_mask = boundary_mask,
                              strategy = strategy, min_spatial_coverage = min_spatial_coverage, 
                              min_temporal_coverage = min_temporal_coverage)