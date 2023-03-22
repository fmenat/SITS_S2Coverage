import os
from utils.read_utils import save_yaml
from tqdm import tqdm


if __name__ == "__main__":
    input_dir = '/ds/images/AI4EO/multi/landcovernet/ref_landcovernet_sa_v1/ref_landcovernet_sa_v1_source_sentinel_2/'
    
    print(f"Starting scanning data from {input_dir}")
    dataset_structure = {}    
    ts_data = sorted(os.listdir(input_dir))
    for ts_i in tqdm(ts_data, total=len(ts_data)):
        if ts_i == "collection.json": 
            continue

        patch_id = "_".join(ts_i.split('_')[7:9])

        if patch_id not in dataset_structure:
            dataset_structure[patch_id] = {"scl_mask_paths":[os.path.join(input_dir,ts_i,'SCL.tif')],  "boundary_paths": None}
        else:
            dataset_structure[patch_id]["scl_mask_paths"].append(os.path.join(input_dir,ts_i,'SCL.tif'))
    print(f"In total {len(dataset_structure)} patches were scanned ")

    output_yaml = './coverage/landcovernet_sa/landcovernet_structure_southamerica.yaml'
    save_yaml(yaml_path=output_yaml, data = dataset_structure)
