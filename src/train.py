import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

from sklearn.metrics import matthews_corrcoef,accuracy_score
from sklearn.ensemble import RandomForestClassifier
def evaluate(y_pred, y_true):
    y_pred_cat = y_pred.argmax(axis=1)
    return {"MCC": matthews_corrcoef(y_true, y_pred_cat), "ACC":accuracy_score(y_true, y_pred_cat)}
    
def performance_by_col(data, col):
    unique_fields = np.unique(data[col].values)
    return_col = {}
    for field in unique_fields:
        mask_field = data[col].values == field
        return_col[field] = evaluate(data["preds"].values[mask_field], data["target"].values[mask_field])
    return return_col

def reconstruct_image_pred(data):
    field_data = np.unique(data["field_names_index"].values)
    pred_data = np.ones((len(field_data), 2000,2000))*np.nan

    for i, d in enumerate(data["preds"].values):
        n = np.where(data.isel(index=i)["field_names_index"].values.tolist() == np.asarray(field_data))[0][0]
        r = data.isel(index=i)["row"].values.tolist()
        c = data.isel(index=i)["col"].values.tolist()
        pred_data[n, r, c] = 1*(d[1]>0.5)
    return pred_data


def save_preds(pred_data, folder, path_names):
    for n in np.arange(len(pred_data)):
        im = Image.fromarray(pred_data[n])
        im.save(f"{folder}/{path_names[n]}.tif")


if __name__ == "__main__":
    P_s = 25
    exp_name = f"predictions_RF_{P_s}x{P_s}"
    data_folder = "/data"
    print("Data will be loaded from ",data_folder, "and will be stored in ",exp_name)
    data_train = xr.open_dataset(f"{data_folder}/train_pixels_data_{P_s}x{P_s}.nc")
    data_train["field_names_index"].loc[{"index":data_train.index}] =  np.vectorize(str)(data_train["field_names_index"])
    print("train data",data_train)
    data_test = xr.open_dataset(f"{data_folder}/test_pixels_data_5x5.nc")
    data_test["field_names_index"].loc[{"index":data_test.index}] =  np.vectorize(str)(data_test["field_names_index"])
    print("test data",data_test)

    model = RandomForestClassifier(n_estimators=100, max_depth=None, oob_score=True, n_jobs=-1)
    model.fit(data_train["s2"].values, data_train["target"].values)
    print("OOB score", model.oob_score_, model.classes_)

    data_train["preds"] = xr.DataArray(model.predict_proba(data_train["s2"].values), dims=["index","y_prob"], coords={"index":data_train.coords["index"].values})
    data_test["preds"] = xr.DataArray(model.predict_proba(data_test["s2"].values), dims=["index","y_prob"], coords={"index":data_test.coords["index"].values})

    data_train.to_netcdf(f"{data_folder}/{exp_name}/train_pixels_data.nc", engine="h5netcdf")
    data_test.to_netcdf(f"{data_folder}/{exp_name}/test_pixels_data.nc", engine="h5netcdf")

    print("Global performance in training" ,evaluate(data_train["preds"].values, data_train["target"].values))
    print("Global performance in testing" ,evaluate(data_test["preds"].values, data_test["target"].values))

    pd.DataFrame.from_dict(performance_by_col(data_train, "field_names_index"), orient="index").to_csv(f"{data_folder}/{exp_name}/train_preds_patchs.csv")
    pd.DataFrame.from_dict(performance_by_col(data_test, "field_names_index"), orient="index").to_csv(f"{data_folder}/{exp_name}/test_preds_patchs.csv")
    print("Save performance by field")
    #preds_train = reconstruct_image_pred(data_train)
    #save_preds(preds_train, f"{data_folder}/{exp_name}/imgs_tr/", np.unique(data_train["field_names_index"].values))
    preds_test = reconstruct_image_pred(data_test)
    save_preds(preds_test,  f"{data_folder}/{exp_name}/imgs_te/", np.unique(data_test["field_names_index"].values))
    print("Save images testing")