# SITS_S2Coverage
[Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) Coverage on Satellite Images Time Series (SITS).

<img src="../imgs/Sentinel2.jpg" alt= “” width="20%">  

> Source: [https://sentinel.esa.int/web/sentinel/missions/sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2)

Based on **Scene Classification Layer** (SCL)  
| Label   | Classification                        |
|---:|:-------------------------|
|  0 | NO_DATA                  |
|  1 | SATURATED_OR_DEFECTIVE   |
|  2 | DARK_AREA_PIXELS         |
|  3 | CLOUD_SHADOWS            |
|  4 | VEGETATION               |
|  5 | NOT_VEGETATED            |
|  6 | WATER                    |
|  7 | UNCLASSIFIED             |
|  8 | CLOUD_MEDIUM_PROBABILITY |
|  9 | CLOUD_HIGH_PROBABILITY   |
| 10 | THIN_CIRRUS              |
| 11 | SNOW                     |



## Execution example for coverage calculation

### Requirements
* tqdm
* rasterio
* numpy
* pandas
* multiprocessing

In order to execute the code to perform the coverage evaluation in a dataset execute [main.py](./main.py). Example is shown below:
```python
idx_targets = [0,1,2,4,5,6,7,10,11] #index to be selected (all except 3, 8 and 9)
min_spatial_coverage=50
min_temporal_coverage=50     
num_process=-1
dataset_structure_path = '/path/to/datasetstructure/seebelow.yaml'
output_dir = "/path/to/output/dir/"
results = analyze_dataset(dataset_structure_path = dataset_structure_path, 
                            idx_targets = idx_targets, 
                            min_spatial_coverage = min_spatial_coverage, 
                            min_temporal_coverage = min_temporal_coverage,
                            output_dir=output_dir,
                            num_process=num_process
                            )
```
> It will store a *.csv* file with the following taxonomy: ```assesment_spat_X_temp_Y_sel_Z_Q.csv```, where X is the *min_spatial_coverage*, Y is the *min_temporal_coverage*, Z is the *idx_targets* parameter filled at two digits each target (e.g. idx_targets=[1,2], then Z="0102"), and Q is the date time in *python datetime* format "YearMonthDayHourMinutesSeconds"

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
You still need to create a yaml file with the following structure:
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

> The name of the files and folder does not affect the calculation. However, the yaml file with the structure of the dataset has to be created. For instance, take a look at [landcovernet_structure_australia.yaml](../coverage/landcovernet_au/landcovernet_structure_australia.yaml) file created by [prepare_landcovernet.py](./prepare_landcovernet.py)
