import os
import rasterio
from src.coverage_analysis.spatial_analyser import SpatialAnalyser

class CoverageAnalysis:
    """
    """
    def __init__(self, timeseries_dir:str, idx_targets:list, boundary_mask:str=None,
                 strategy:str='by_clouds',min_spatial_coverage:int=50, min_temporal_coverage:int=50):
        """Make analysis for the whole timeserie of one patch
        
        strategy: Options -> 'by_clouds', 'by_classes'
        """
        #super(CoverageAnalysis,self).__init__()
        self.timeseries_dir = timeseries_dir
        self.strategy = strategy
        self.min_spatial_coverage = min_spatial_coverage
        self.min_temporal_coverage = min_temporal_coverage
        self.idx_targets = idx_targets
        self.boundary_mask = boundary_mask

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
        for ts in os.listdir(self.timeseries_dir):
            if ts.endswith('.tif') or ts.endswith('.tiff') or ts.endswith('.TIF') or ts.endswith('.TIFF'):
                total_ts+=1
                #read data
                ts_path = os.path.join(self.timeseries_dir,ts)
                ts_raster = rasterio.open(ts_path)
                #spatial coverage
                spatial_cov = self._spatial_coverage(ts_raster)
                spatial_cov_accumulated.append(spatial_cov)
                #temporal coverage
                if spatial_cov >= self.min_spatial_coverage:
                    temporal_cov_counter.append(ts)
            else:raise ValueError("Unexpected file extention for", ts)
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
    
    def _spatial_coverage(self,scl_mask):
        '''Analyses a single field, deliveres cloud and vegetate-non vegetated coverage
        
        Args:
            scl_mask_path: path to SCL mask classification from S2
            yield_mask_path: path to yield mask

        Returns:
            cloud_coverage (float): percentage of field covered by clouds class.
            veg_non_veg_coverage (float): percentage of field covered by vegetated and non vegetated clas.
        '''
        spatial_analyser_ = SpatialAnalyser(scl_mask, self.idx_targets, self.boundary_mask)
        percentage = spatial_analyser_.target_analysis()
        if self.strategy=='by_clouds':
            spatial_cov = 100 - percentage
        elif self.strategy=='by_classes':
            spatial_cov = percentage
        else: raise ValueError("Unexpected value of 'strategy'!", self.strategy)
        return spatial_cov
