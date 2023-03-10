import rasterio
import numpy as np
from scipy import interpolate

class SpatialAnalyser:
    def __init__(self, scl_mask:rasterio, idx_targets:list, boundary_mask:rasterio=None):
        '''
        Args:
            scl_mask: scl mask from s2 image used for filtering e.g. vegetated and not_vegetated
            idx_targets: index(es) for clouds in scl mask
            idx_targets (optional): index(es) for specific class(es) in scl mask. E.g. 4:'vegetation', 5:'not_vegetated'
            boundary_mask (optional): mask for specific objects inside image.

        '''
        self.scl_mask_arr = scl_mask.read(1)
        self.idx_targets = idx_targets 
        if boundary_mask is not None:
            self.boundary_mask = boundary_mask
            self.boundary_mask_arr = self.boundary_mask.read(1) 
            self.boundary_mask_nodata = self.boundary_mask.meta['nodata']
            scl_res, boundary_res = list(scl_mask.res), list(self.boundary_mask.res)
            if scl_res != boundary_res:
                window_size = int(scl_res[0] / boundary_res[0]) # 4
                self.boundary_mask_arr = self._bicubic_interp(self.boundary_mask_arr, window_size)
        else:self.boundary_mask = None
        
   
    def target_analysis(self):
        return self._percentage_given_scl_idx(filter_=self.idx_targets)

    def _percentage_given_scl_idx(self,filter_):
        '''Get percentage of data used according to SCL mask class index used.

        Args:
            filter_: class indexes to filter scl_mask and make the percentage analysis.
        
        '''
        total_size = self.scl_mask_arr.shape[0] * self.scl_mask_arr.shape[1]
        if self.boundary_mask is not None:
            #mask based on data available inside boundary
            self.scl_mask_arr[np.where(self.boundary_mask_arr == self.boundary_mask_nodata)] = 0 #assigning '0' (no_data) in scl_mask to the pixels outside the boundary  
            total_size = total_size - np.sum(self.boundary_mask_arr == self.boundary_mask_nodata)
        #mask based on scl mask index
        bool_mask = np.zeros(self.scl_mask_arr.shape)
        bool_mask = self._mask_array_from_list(arr1=bool_mask, arr2=self.scl_mask_arr, filter_=filter_)
        bool_mask_count = np.sum(bool_mask==1)
        #percentage of data used with respect to the image
        percentage = round(bool_mask_count * 100 / total_size,2)
        #print(percentage)
        return percentage
    
    @staticmethod
    def _bicubic_interp(data, factor =4):
        W, H= data.shape
        f = interpolate.RectBivariateSpline(np.arange(0, W), np.arange(0, H), data, kx=3, ky=3)
        x = np.arange(0, W, factor)
        y = np.arange(0, H, factor)
        return f(x,y)

    @staticmethod
    def _mask_array_from_list(arr1:np.array, arr2:np.array, filter_:list):
        '''Filter array1 based on filter values found in array2.

        '''
        for idx in filter_:
            arr1[np.where(arr2==idx)] = 1
        return arr1