# SITS_S2Coverage
[Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) Coverage on Satellite Images Time Series (SITS).

<img src="../imgs/Sentinel2.jpg" alt= “” width="20%">  

> Source: [https://sentinel.esa.int/web/sentinel/missions/sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2)

Based on **Scene Classification Layer** (SCL)

<img src="../imgs/scl.png" alt= “” width="30%">

> Source: [https://docs.astraea.earth/hc/en-us/articles/360051409652-Masking-Sentinel-2-L2A-Using-RasterFrames](https://docs.astraea.earth/hc/en-us/articles/360051409652-Masking-Sentinel-2-L2A-Using-RasterFrames)


## Execution example for coverage calculation

### Requirements
* tqdm
* rasterio
* numpy
* pandas
* multiprocessing

In order to execute the code to perform the coverage evaluation in a dataset execute [main.py](./main.py). Example is shown below:
```python
dataset_structure_path = '/path/to/datasetstructure/seebelow.yaml'
strategy= 'by_classes' or 'by_clouds'
idx_targets = [4,5] (for vegetated filtering - by classes) [8,9,3] (for cloud filtering - by clouds)
min_spatial_coverage=50
min_temporal_coverage=50      
output_dir = "/path/to/output/dir/"
num_process=-1
results = analyze_dataset(dataset_structure_path = dataset_structure_path, 
                            idx_targets = idx_targets, 
                            strategy = strategy, 
                            min_spatial_coverage = min_spatial_coverage, 
                            min_temporal_coverage = min_temporal_coverage,
                            output_dir=output_dir,
                            num_process=num_process
                            )
```
> It will store a *.csv* file with the following taxonomy: ```assesment_X_spatial_Y_temporal_Z.csv```, where Y is the *min_spatial_coverage*, Z is the *min_temporal_coverage* and X is the *strategy* parameter.

Please be aware that independently of how the data is organized, e.g. like
```
data
├── patch_id1
│   ├── s2_images
│   │   ├── images_id1_S2_time1.tif
│   │   ├── images_id1_S2_time2.tif
│   │   └── . . .
│   └── scl_mask
│       ├── images_id1_SCLmask_time1.tif
│       ├── images_id1_SCLmask_time2.tif
│       └── . . .
├── patch_id2
└── patch_id3
└── . . .
```
You still needs to create a yaml file with the following structure:
```
patch_id1: 
    boundary_paths: null
    scl_mask_paths:
        - /path/to/images_id1_SCLmask_time1.tif
        - /path/to/images_id1_SCLmask_time2.tif
        - /path/to/images_id1_SCLmask_time3.tif
        . . .
patch_id2: 
    boundary_paths: null
    scl_mask_paths:
        - /path/to/images_id2_SCLmask_time1.tif
        - /path/to/images_id2_SCLmask_time2.tif
        - /path/to/images_id2_SCLmask_time3.tif
        . . .
. . .          
```

> The name of the files and folder does not affect the calculation. However, the yaml file with the structure of the dataset has to be created. See the examples at [landcovernet_structure_australia.yaml](../coverage/landcovernet_au/landcovernet_structure_australia.yaml), created by [prepare_landcovernet.py](./prepare_landcovernet.py)
