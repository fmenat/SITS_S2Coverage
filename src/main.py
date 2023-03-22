from src.coverage_analysis.dataset_coverage_analysis import analyze_dataset
from src.coverage_analysis.SCL import IND_ALL_,IND_CLOUDS_, remove_labels


if __name__ == "__main__":
    dataset_structure_path = './coverage/landcovernet_sa/landcovernet_structure_southamerica.yaml'
    output_dir = "./coverage/landcovernet_sa/"
    
    idx_targets = remove_labels(IND_ALL_, IND_CLOUDS_) #index to be selected (all except 3, 8 and 9)
    min_spatial_coverage=50
    min_temporal_coverage=50      
    num_process=-1

    print(f"Starting execution from {dataset_structure_path}")
    results = analyze_dataset(dataset_structure_path = dataset_structure_path, 
                                idx_targets = idx_targets, 
                                min_spatial_coverage = min_spatial_coverage, 
                                min_temporal_coverage = min_temporal_coverage,
                                output_dir=output_dir,
                                num_process=num_process
                                )