import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import rasterio
import os, time
from tqdm import tqdm
from pathlib import Path
from scipy import interpolate

import multiprocessing as mp
from functools import partial
def mp_proxy(iterable, func,static_func_kwargs={}, map_type="imap", context="fork", processes=-1, chunksize=1):
    if processes == -1:
        processes = int(len(os.sched_getaffinity(0))/2)
    print(f"spawning {processes} processes")

    with mp.get_context(context).Pool(processes=processes) as pool:
        if map_type == "imap":
            map_func = pool.imap
        elif map_type == "imap_unordered":
            map_func = pool.imap_unordered
        res = map_func(partial(func,  **static_func_kwargs), iterable, chunksize=chunksize)
        for res_i in res:
            yield res_i



def process_read(folder_path):
    x_i= []
    for times_f in sorted(Path(folder_path / "s2_images").iterdir()):  
        with rasterio.open(str(times_f)) as t:
            x_i.append(t.read().transpose([1,2,0]))

    clm_i = []
    for times_f in sorted(Path(folder_path / "clm_masks").iterdir()):
        with rasterio.open(str(times_f)) as t:
            clm_i.append(t.read().transpose([1,2,0]))

    isdata_i = []
    for times_f in sorted(Path(folder_path / "is_data_masks").iterdir()): 
        with rasterio.open(str(times_f)) as t:
            isdata_i.append(t.read().transpose([1,2,0]))

    with rasterio.open( str(Path(folder_path / "CULTIVATED.tif"))) as t:
        y_data = t.read().transpose([1,2,0])

    return {
         "field": folder_path.stem, 
         "s2_images": np.stack(x_i, axis=0),
         "cloud_mask": np.stack(clm_i, axis=0),
         "is_data_mask": np.stack(isdata_i, axis=0),
         "cultivated": y_data,
         }

def bicubic_interp(data, res =4):
    W, H= data.shape
    f = interpolate.RectBivariateSpline(np.arange(0, W), np.arange(0, H), data, kx=3, ky=3)
    x = np.arange(0, W, 1/res)
    y = np.arange(0, H, 1/res)
    return f(x,y)

def calculate_features_window(data, axis=1):
    stats_calc = [np.nanmin, np.nanmax, np.nanmean, np.nanmedian, np.nanstd, lambda x,axis: np.nanpercentile(x, 25, axis=axis), lambda x,axis: np.nanpercentile(x, 75,axis=axis)]
    stats_ =  [s_func(data, axis=axis) for s_func in stats_calc]
    return stats_ + [stats_[1]-stats_[0],]
    
def process_patch(folder_path, verbose=False, mode_train=False, res=4, P_s=25):
    if not mode_train:
        if os.path.exists(f"/data/temporary_pixels_test/{str(folder_path.stem)}_pixels_{P_s}x{P_s}.nc"):
            print("Skipping file ",folder_path)
            return []

    print(f"Starting for {folder_path}")
    start_time = time.time()

    i = process_read(folder_path)
    S2_data = i["s2_images"]
    CLM_mask = i["cloud_mask"]
    ISD_mask = i["is_data_mask"]
    Y_mask = i["cultivated"]
    fields_data = i["field"]
    
    #increase image size bicubally interpolated x4 upscaling
    S2_upsample = np.ones((S2_data.shape[0],2000,2000, S2_data.shape[-1]),dtype=np.float32)*np.nan
    CLM_mask_upsample = np.ones((CLM_mask.shape[0],2000,2000, 1),dtype=np.float32)
    ISD_mask_upsample = np.ones((ISD_mask.shape[0],2000,2000, 1),dtype=np.float32)
    for t in range(S2_upsample.shape[0]):
        if t % 5 == 0 and verbose:
            print("Interpolating now in ",t, "with time ",time.time()-start_time)
        CLM_mask_upsample[t,:,:,0] = np.maximum(0, bicubic_interp(CLM_mask[t,:,:,0],res=res)).astype(np.float32)
        ISD_mask_upsample[t,:,:,0] = np.maximum(0, bicubic_interp(ISD_mask[t,:,:,0],res=res)).astype(np.float32)
        for b in range(S2_upsample.shape[-1]):
            S2_upsample[t,:,:,b] = np.maximum(0,bicubic_interp(S2_data[t,:,:,b],res=res)).astype(np.float32)
    if verbose:
        print("Finished interpolating for one field with ",time.time()-start_time)
    S2_data = S2_upsample
    CLM_mask = CLM_mask_upsample
    ISD_mask = ISD_mask_upsample

   
    S2_data[ CLM_mask[:,:,:,0] >0.5 ] = np.nan  #mask clouds
    S2_data[ ISD_mask[:,:,:,0] ==0 ] = np.nan #Is data mask
    ISD_mask = ISD_mask.sum(axis=(0,3))
    CLM_mask = CLM_mask.mean(axis=(0,3))
    if verbose:
        print("Finished masking for one field",time.time()-start_time)

    _, W, H, _ = S2_data.shape
    w = int((P_s-1)/2)
    X_pixel = []
    Y_pixel = []
    row_train = []
    col_train = []
    field_indexs = []
    for i in np.arange(0, W, res if mode_train else 1):
        for j in np.arange(0, H, res if mode_train else 1):
            if ISD_mask[i,j] == 0:
                continue
            if CLM_mask[i,j] > 0.5 and mode_train:
                continue
            field_indexs.append(fields_data)
            row_train.append(i)
            col_train.append(j)
            x_lim1 = max([i-w, 0])
            x_lim2 = min([i+w+1, W])
            y_lim1 = max([j-w, 0])
            y_lim2 = min([j+w+1, H])
            X_pixel.append( np.concatenate( calculate_features_window(S2_data[:,x_lim1:x_lim2,y_lim1:y_lim2,:], axis=(0,1,2)) ))
            Y_pixel.append( Y_mask[i,j] )
        if verbose:
            print("all columns for one row were executed, now in ", i, " with ",time.time()-start_time)
    print(f"Finished for {folder_path}")

    data_vars = dict(
        s2 = xr.DataArray(np.asarray(X_pixel), dims=["index","features"], coords={"index":np.arange(len(X_pixel)), "features":np.arange(12*8)}),
        target = xr.DataArray(np.asarray(Y_pixel)[:,0], dims=["index"], coords={"index":np.arange(len(X_pixel))}),
        col = xr.DataArray(col_train, dims=["index"], coords={"index":np.arange(len(X_pixel))}),
        row = xr.DataArray(row_train, dims=["index"], coords={"index":np.arange(len(X_pixel))}),
        field_names_index = xr.DataArray(field_indexs, dims=["index"], coords={"index":np.arange(len(X_pixel))})
        )
    data_train = xr.Dataset(data_vars=data_vars)
    if mode_train:
        data_train.to_netcdf(f"/data/temporary_pixels_train/{str(folder_path.stem)}_pixels_{P_s}x{P_s}.nc", engine="h5netcdf")
    else:
        data_train.to_netcdf(f"/data/temporary_pixels_test/{str(folder_path.stem)}_pixels_{P_s}x{P_s}.nc", engine="h5netcdf")

    return dict(
        X_pixel = X_pixel,
        Y_pixel = Y_pixel,
        row_train= row_train,
        col_train = col_train,
        field_indexs = field_indexs
    )


FLAG = "test"
PIXELS_ = 25
if __name__ == "__main__":
    print("EXECUTING IN ",FLAG,"MODE WITH PIXELS =",PIXELS_)
    data_folder = "/data"
    folder = f"{data_folder}/preprocessed/train"
    paths_path = sorted(Path(folder).iterdir())
    
    indx_all = np.arange(len(paths_path))
    np.random.seed(0)
    field_test = np.random.choice(paths_path, size=20, replace=False)
    field_train = [f for f in paths_path if f not in field_test]
    if FLAG == "train":
        TRAIN_FLAG = True
        fields_ = field_train
    elif FLAG == "test":
        TRAIN_FLAG = False
        fields_ = field_test
    else:#all
        TRAIN_FLAG = False
        fields_ = paths_path
    print("Selecting ",len(fields_),"images for execution, e.g. :",fields_[:5])

    mp_inst = mp_proxy(
        iterable=fields_,
        func=process_patch,
        static_func_kwargs={
            'verbose': False,
            "mode_train": TRAIN_FLAG,
            "P_s": PIXELS_,
            },
        map_type="imap",
        context="spawn", #spawn, fork
        processes=-1,
        chunksize=1,
        )

    X_pixel = [] 
    Y_pixel = []
    row_train= []
    col_train = []
    field_indexs = []
    for i in tqdm(mp_inst):
        if len(i) == 0:
            continue
        X_pixel.extend(i["X_pixel"])
        Y_pixel.extend(i["Y_pixel"])
        row_train.extend(i["row_train"])
        col_train.extend(i["col_train"])
        field_indexs.extend(i["field_indexs"])

    data_vars = dict(
        s2 = xr.DataArray(np.asarray(X_pixel), dims=["index","features"], coords={"index":np.arange(len(X_pixel)), "features":np.arange(12*8)}),
        target = xr.DataArray(np.asarray(Y_pixel)[:,0], dims=["index"], coords={"index":np.arange(len(X_pixel))}),
        col = xr.DataArray(col_train, dims=["index"], coords={"index":np.arange(len(X_pixel))}),
        row = xr.DataArray(row_train, dims=["index"], coords={"index":np.arange(len(X_pixel))}),
        field_names_index = xr.DataArray(np.asarray(field_indexs).tolist(), dims=["index"], coords={"index":np.arange(len(X_pixel))})
        )
    data_train = xr.Dataset(data_vars=data_vars)

    print(data_train)
    data_train.to_netcdf(f"{data_folder}/{FLAG}_pixels_data_{PIXELS_}x{PIXELS_}.nc", engine="h5netcdf")
