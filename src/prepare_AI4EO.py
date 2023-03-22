import os
from pathlib import Path
from utils.read_utils import save_yaml, read_npy_gz, read_pkl_gz
from utils.dir_utils import create_dir
import numpy as np
import rasterio
from rasterio.transform import Affine
from tqdm import tqdm

def create_tif(arr:np.array, output_path:str, bbox, xres, yres):
    """Converts array into raterio object and save as tiff file.
    """
    Z = arr.copy()
    transform = Affine.translation(list(bbox)[0], list(bbox)[1]+(Z.shape[1]*xres)) * Affine.scale(xres, yres) * Affine.rotation(-90)
    if Z.dtype == 'bool':
        Z = Z.astype(np.uint8)
    with rasterio.open(output_path,
            mode="w",
            driver="GTiff",
            height=Z.shape[1],
            width=Z.shape[0],
            count=Z.shape[-1],
            dtype=Z.dtype,
            crs=str(bbox.crs),
            transform=transform,
            ) as new_dataset: 
        new_dataset.write(np.moveaxis(Z, [0, 1, 2], [2, 1, 0]))

def aggregated_array_to_files(patch_path,arr,bbox):
    for i in range(arr.shape[0]):
        scl_time_step = arr[i] #arr[i,:, :, 0]
        scl_time_step_path = os.path.join(patch_path,'ts_'+str(i).zfill(3)+'.tif')
        create_tif(scl_time_step,scl_time_step_path,bbox,10,10)

if __name__ == "__main__":
    dataset_dir = '/ds/images/AI4EO/EnhancedS2Agriculture/raw/'
    dataset_type = 'train' #'test'
    input_dir = os.path.join(dataset_dir,dataset_type)
    temp_restructured_folder = create_dir(os.path.join(str(Path(input_dir).parent),dataset_type+'_s2coverage_restructured_temp'))
    patches_ids =  sorted(os.listdir(input_dir))
    dataset_structure =  dict.fromkeys(patches_ids, {})
    print(patches_ids)
    for patch_id in tqdm(patches_ids, total=len(patches_ids)):
        new_patch_path = create_dir(os.path.join(temp_restructured_folder,patch_id))
        scl_aggregated_array = read_npy_gz(os.path.join(input_dir,patch_id,'mask','SCL.npy.gz'))
        bbox = read_pkl_gz(os.path.join(input_dir,patch_id,'bbox.pkl.gz'))
        aggregated_array_to_files(new_patch_path,scl_aggregated_array,bbox)
        scl_mask_paths = [os.path.join(new_patch_path,file) for file in os.listdir(new_patch_path)]
        dataset_structure[patch_id] = {'scl_mask_paths': sorted(scl_mask_paths), 'boundary_paths': None}
    print(f"In total {len(patches_ids)} patches were scanned ")

    output_yaml = f"./coverage/ai4eo/ai4eo_structure_{dataset_type}.yaml"
    save_yaml(yaml_path=output_yaml, data = dataset_structure)

