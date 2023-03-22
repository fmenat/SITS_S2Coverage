# SITS_S2Coverage
[Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) Coverage on Satellite Images Time Series (SITS).

<img src="imgs/Sentinel2.jpg" alt= “” width="20%">  

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



## AI4EO - Enhanced Agriculture challenge
The task is to provide a *cultivated or not* map (binary classification) at a higher resolution (2.5m) than the input Sentinel-2 SITS (10m). The data belongs to Slovenia country.

* Data: https://platform.ai4eo.eu/enhanced-sentinel2-agriculture-permanent/data
* Sources: https://github.com/AI4EO/enhanced-sentinel2-agriculture-challenge
* Baseline used: Tarasiewicz, T., Tulczyjew, L., Myller, M., Kawulok, M., Longépé, N., & Nalepa, J. (2022, July). *Extracting High-Resolution Cultivated Land Maps from Sentinel-2 Image Series*. In IGARSS 2022-2022 IEEE International Geoscience and Remote Sensing Symposium (pp. 175-178). IEEE. DOI: [10.1109/IGARSS46834.2022.9883919](https://doi.org/10.1109/IGARSS46834.2022.9883919)


> Product generated  
* Prediction Performance by Patch: [ml_results/ai4eo](ml_results/ai4eo)
* Outcome (Coverage result): [coverage/ai4eo](coverage/ai4eo)

*sample from [assesment_spat_70_temp_70_sel_0405.csv](coverage/ai4eo/assesment_spat_70_temp_70_sel_0405.csv)*:
|filename |num_timesteps | num_timesteps_missing | avg_spatial_coverage | num_timesteps_abovecov | temporal_coverage | assesment_temporal | assesment_spatial |
| ---        | --- | ---| ---   | ---|---    | ---  | --- |
|eopatch-841 | 38  | 38 | 81.87 | 30 | 78.95 | high | high|
|eopatch-781 | 38  | 38 | 73.21 | 23 | 60.53 | low  | high|
|eopatch-718 | 38  | 38 | 61.21 | 18 | 47.37 | low  | low |
| ...        | ... | ...| ...  | ... | ... | ... | ... |

## LandCoverNet  - Europe
The task is to provide a land-cover map (a classification based on 7 classes) at 10m resolution. The data is global but distributed in different regions where we executed the assessment: Africa, Asia, Australia, Europe, North America, and South America.

* Data source: https://mlhub.earth/data/ref_landcovernet_eu_v1
* Reference: Alemohammad, H., & Booth, K. (2020). *LandCoverNet: A global benchmark land cover classification training dataset*. arXiv preprint [arXiv:2012.03111](https://arxiv.org/abs/2012.03111).

> Product generated  
* Outcome in Africa (Coverage result): [coverage/landcovernet_af](coverage/landcovernet_af)
* Outcome in Asia (Coverage result): [coverage/landcovernet_as](coverage/landcovernet_as)
* Outcome in Australia (Coverage result): [coverage/landcovernet_au](coverage/landcovernet_au)
* Outcome in Europe (Coverage result): [coverage/landcovernet_eu](coverage/landcovernet_eu)
* Outcome in North America (Coverage result): [coverage/landcovernet_na](coverage/landcovernet_na)
* Outcome in South America (Coverage result): [coverage/landcovernet_sa](coverage/landcovernet_sa)


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