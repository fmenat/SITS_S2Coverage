# SITS_S2Coverage
[Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) Coverage on Satellite Images Time Series (SITS).

![alt text](https://github.com/fmenat/sits_s2coverage/blob/main/imgs/Sentinel2.jpg?raw=true)
> Source: [https://sentinel.esa.int/web/sentinel/missions/sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2)

Based on **Scene Classification Layer** (SCL)

![alt text](https://github.com/fmenat/sits_s2coverage/blob/main/imgs/scl.png?raw=true)
> Source: [https://docs.astraea.earth/hc/en-us/articles/360051409652-Masking-Sentinel-2-L2A-Using-RasterFrames](https://docs.astraea.earth/hc/en-us/articles/360051409652-Masking-Sentinel-2-L2A-Using-RasterFrames)


## Execution example for coverage calculation

### Requirements
* tqdm
* rasterio
* numpy
* pandas

In order to execute the code for perform the coverage evaluation in a dataset execute:
```python
input_dir = '/path/to/folder/with/timeseriesimages'
boundary_mask=None
strategy= 'by_clouds' #'by_classes' or 'by_clouds'
idx_targets = [8,9,3] #[4,5]
min_spatial_coverage=50
min_temporal_coverage=50      
results = analyse_dataset(input_dir = input_dir, idx_targets = idx_targets, boundary_mask = boundary_mask,
                          strategy = strategy, min_spatial_coverage = min_spatial_coverage, 
                          min_temporal_coverage = min_temporal_coverage)
```

Please be aware that the data has to be organized on the following format:
```
data
├── images_id1
│   ├── s2_images
│   │   ├── images_id1_S2_time1.tif
│   │   ├── images_id1_S2_time2.tif
│   │   └── . . .
│   └── scl_mask
│       ├── images_id1_SCLmask_time1.tif
│       ├── images_id1_SCLmask_time2.tif
│       └── . . .
├── images_id2
└── images_id3
└── . . .
```
The name of the files and folder does not affect the calculation. However the Sentinel-2 images has to be in a folder named **s2_images** inside each patch, while SCL has to be in a folder named **scl_mask**.
