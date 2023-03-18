import os
import rasterio
from src.coverage_analysis.spatial_analyzer import SpatialAnalyzer

FILE_EXTENSIONS = ['.tif', '.tiff', '.TIF', '.TIFF']

class CoverageAnalysis:
    """
    """
    def __init__(self, 
                 scl_mask_paths:list, 
                 idx_targets:list, 
                 boundary_paths:list=None,
                 min_spatial_coverage:int=50, 
                 min_temporal_coverage:int=50
                 ):
        """Make analysis for the whole timeserie of one patch
        
        """
        #super(CoverageAnalysis,self).__init__()
        self.scl_mask_paths = scl_mask_paths
        self.min_spatial_coverage = min_spatial_coverage
        self.min_temporal_coverage = min_temporal_coverage
        self.idx_targets = idx_targets
        self.boundary_paths = boundary_paths

    def temporal_spatial_coverage(self):
        total_ts = 0
        spatial_cov_accumulated = []
        #init_assesment dictionary
        assesment_dict = { 'num_timesteps': None,
                            'num_timesteps_missing': None,
                            'avg_spatial_coverage':None,
                            'num_timesteps_abovecov': None,
                            'temporal_coverage': None,  
                            'assesment_temporal': None,
                            'assesment_spatial': None,
                            }
        #timeserie analysis
        temporal_cov_counter = []
        for idx,scl_mask in enumerate(self.scl_mask_paths):
            if scl_mask.endswith(tuple(FILE_EXTENSIONS)):
                total_ts+=1
                #read data
                scl_mask_raster = rasterio.open(scl_mask)
                if self.boundary_paths is not None:
                    boundary_mask_raster = rasterio.open(self.boundary_paths[idx])
                else:boundary_mask_raster=None
                #spatial coverage
                spatial_cov = self._spatial_coverage(scl_mask_raster,boundary_mask_raster)
                spatial_cov_accumulated.append(spatial_cov)
                #temporal coverage
                if spatial_cov >= self.min_spatial_coverage:
                    temporal_cov_counter.append(scl_mask)
            else:raise ValueError("Unexpected file extention for", scl_mask)
        temporal_cov = len(temporal_cov_counter)*100/ total_ts
        #fill assement dictionary - temporal coverage
        assesment_dict['temporal_coverage'] = temporal_cov
        assesment_dict['num_timesteps'] = total_ts
        assesment_dict["num_timesteps_missing"] = len([ None for v in spatial_cov_accumulated if v!=100])
        assesment_dict["num_timesteps_abovecov"] = len(temporal_cov_counter)
        if temporal_cov >= self.min_temporal_coverage:
                assesment_dict['assesment_temporal'] = 'high'
        else: assesment_dict['assesment_temporal'] = 'low'
        #fill assement dictionary - spatial coverage
        #print(spatial_cov_accumulated)
        avg_spatial_coverage = sum(spatial_cov_accumulated)/len(spatial_cov_accumulated)
        assesment_dict['avg_spatial_coverage'] = avg_spatial_coverage
        if avg_spatial_coverage >= self.min_spatial_coverage:
                assesment_dict['assesment_spatial'] = 'high'
        else: assesment_dict['assesment_spatial'] = 'low'
        return assesment_dict
    
    def _spatial_coverage(self,scl_mask,boundary_mask):
        '''It analyzes a single field, deliveres cloud and vegetate-non vegetated coverage
        
        Args:
            scl_mask_path: path to cloud mask classification from S2
            yield_mask_path: path to yield mask

        Returns:
            cloud_coverage (float): percentage of field covered by clouds class.
            veg_non_veg_coverage (float): percentage of field covered by vegetated and non vegetated clas.
        '''
        spatial_analyzer_ = SpatialAnalyzer(scl_mask, self.idx_targets, boundary_mask)
        spatial_cov = spatial_analyzer_.target_analysis()
        return spatial_cov
