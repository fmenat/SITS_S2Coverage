# SITS_S2Coverage
[Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) Coverage on Satellite Images Time Series (SITS).

![alt text](https://github.com/fmenat/sits_s2coverage/blob/main/imgs/Sentinel2.jpg?raw=true)
> Source: [https://sentinel.esa.int/web/sentinel/missions/sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2)

Based on **Scene Classification Layer** (SCL)

![alt text](https://github.com/fmenat/sits_s2coverage/blob/main/imgs/scl.png?raw=true)
> Source: [https://docs.astraea.earth/hc/en-us/articles/360051409652-Masking-Sentinel-2-L2A-Using-RasterFrames](https://docs.astraea.earth/hc/en-us/articles/360051409652-Masking-Sentinel-2-L2A-Using-RasterFrames)


## AI4EO - Enhanced Agriculture challenge
The task is to provide a *cultivated or not* map (binary classification) at a higher resolution (2.5m) than the input Sentinel-2 SITS (10m). The data belongs to Slovenia country.

* Data: https://platform.ai4eo.eu/enhanced-sentinel2-agriculture-permanent/data
* Sources: https://github.com/AI4EO/enhanced-sentinel2-agriculture-challenge
* Baseline used: Tarasiewicz, T., Tulczyjew, L., Myller, M., Kawulok, M., Longépé, N., & Nalepa, J. (2022, July). *Extracting High-Resolution Cultivated Land Maps from Sentinel-2 Image Series*. In IGARSS 2022-2022 IEEE International Geoscience and Remote Sensing Symposium (pp. 175-178). IEEE. DOI: [10.1109/IGARSS46834.2022.9883919](https://doi.org/10.1109/IGARSS46834.2022.9883919)


> Prediction Performance by Patch: [result/ai4eo](result/ai4eo)
> Outcome (Coverage result): [coverage/ai4eo](coverage/ai4eo)

*sample from [assesment_report_veg_70_70.csv](coverage/ai4eo/assesment_report_veg_70_70.csv)*:
|filename |num_timesteps | num_timesteps_missing | avg_spatial_coverage | num_timesteps_abovecov | temporal_coverage | assesment_temporal | assesment_spatial |
| ---        | --- | ---| ---   | ---|---    | ---  | --- |
|eopatch-841 | 38  | 38 | 81.87 | 30 | 78.95 | high | high|
|eopatch-781 | 38  | 38 | 73.21 | 23 | 60.53 | low  | high|
|eopatch-718 | 38  | 38 | 61.21 | 18 | 47.37 | low  | low |
| ...        | ... | ...| ...  | ... | ... | ... | ... |

## LandCoverNet  - Europe
The task is to provide a land-cover map (7 class classification) at XX resolution. The data belongs to the Europe continent.

* Data source: https://mlhub.earth/data/ref_landcovernet_eu_v1
* Reference: Alemohammad, H., & Booth, K. (2020). *LandCoverNet: A global benchmark land cover classification training dataset*. arXiv preprint [arXiv:2012.03111](https://arxiv.org/abs/2012.03111).

> Outcome: [coverage/landcovernetEU](coverage/landcovernetEU)

sample?


## Execution example
For examples on execution go to [src/README.md](src/README.md)


## Authors and acknowledgment
Cristhian Sanchez and Francisco Mena. 


## Citation
Not published yet.


## Licence

Copyright (C) 2022 authors of this github.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.