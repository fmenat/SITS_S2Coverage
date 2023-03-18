import os
from utils.read_utils import save_yaml

if __name__ == "__main__":
    input_dir = '/ds/yieldcon/yieldData/VI-delivery/Argentina/MX_First/'
    ignore_in_dir = ['web', 'skipped_files.txt', 'zz_report']
    patches_ids = [patch for patch in os.listdir(input_dir) if patch not in ignore_in_dir]
    dataset_structure =  dict.fromkeys(patches_ids, {})
    print(patches_ids)
    for patch_id in patches_ids:
        print(patch_id,'___')
        scl_patch_path = os.path.join(input_dir,patch_id,'scl_masks')
        scl_paths = [os.path.join(scl_patch_path,file) for file in os.listdir(os.path.join(scl_patch_path))]
        dataset_structure[patch_id] = {'scl_mask_paths': scl_paths, 'boundary_paths': None}
    print(f"In total {len(patches_ids)} patches were scanned ")

    save_yaml(yaml_path='../coverage/YC/MX_First.yaml', data = dataset_structure)
