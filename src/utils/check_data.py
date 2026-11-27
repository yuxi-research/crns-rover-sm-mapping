#%% Test saved raster
import os
import xarray as xr
import rioxarray as rxr
import pandas as pd
import geopandas as gpd


PASS = "✓"
FAIL = "✗"
WARN = "⚠"
INFO = "ℹ"

#%% check raster file
def check_raster(da, show_info=False):
    """
    Check a raster file by checking its existence, ability to be opened, data presence, CRS, and transform.
    Parameters:
    da (xarray.DataArray or xarray.Dataset, or str): The raster file path or RioXarray DataArray/Dataset to check.
    show_info (bool): Whether to print raster information.
    """

    # Raster exists

    if isinstance(da, str):
            assert os.path.exists(da), f"{FAIL} Raster file does not exist: {da}"
            da = rxr.open_rasterio(da).squeeze('band', drop=True)

    if isinstance(da, xr.Dataset):
        print(f"########### Validating variables in Dataset ############")
        for var in da.data_vars:
            assert da[var].rio.crs == da.rio.crs, f"{FAIL} Variable {var} has a different CRS."
            assert da[var].rio.transform() == da.rio.transform(), f"{FAIL} Variable {var} has a different transform."
            # check each variable in the Dataset  as a DataArray
            check_raster(da[var], show_info=show_info)
            
        print(f"{PASS} Dataset is valid.")
        del da
        print('########################################################')
        return None  # Return None after validating all variables in the Dataset

    elif isinstance(da, xr.DataArray):
        assert da is not None, f"{FAIL} Raster DataArray is None"

    else:
        raise TypeError(f"Expected a file path, DataArray, or Dataset, got {type(da)}")


    # Raster can be opened
    assert da is not None, f"{FAIL} Raster could not be opened."

    # Raster has data
    assert da.size > 0, f"{FAIL} Raster has no data."

    # CRS exists
    assert da.rio.crs is not None, f"{FAIL} Raster has no CRS."

    # transform exists
    assert da.rio.transform() is not None, f"{FAIL} Raster has no transform."

    # Print 
    print(f"{PASS} DataArray is valid.")
    
    if show_info:
        # Get grid resolution
        print('======== DataArray Info ========')
        print('CRS:\t', da.rio.crs)
        print('Shape:\t', da.shape)
        print("Indexes dims:\t", da.indexes.dims)
        print("x[0], x[-1], lon increment:\t", da.x.values[0], da.x.values[-1], da.x[1].values - da.x[0].values)
        print("y[0], y[-1], lat increment:\t", da.y.values[0], da.y.values[-1], da.y[1].values - da.y[0].values)
        print('Bounds:\t', da.rio.bounds())
        print('No data value:\t', str(da.rio.nodata))

        print(da.coords)
        print("attrs:\n", da.attrs)

        if da.shape[0] > 5 and da.shape[1] > 5:
            print('5x5 center data sample:\n', 
                da[da.shape[0]//2-2:da.shape[0]//2+3, da.shape[1]//2-2:da.shape[1]//2+3].values)
        else:
            print('Data sample:\n', da.values)
        print('================================')


    del da
    return True

# %% check GeoDataFrame
# import geopandas as gpd
def check_gdf(gdf, show_info=False):
    """
    check a GeoDataFrame by checking its type, index uniqueness, column uniqueness, CRS, and geometry validity.

    Parameters:
    gdf (gpd.GeoDataFrame or str): The GeoDataFrame to check or the path to a file that can be read into a GeoDataFrame.
    show_info (bool): Whether to print geodataframe information.
    Returns: If the input is a file path, returns the loaded GeoDataFrame; otherwise, returns None
    """
    if isinstance(gdf, str):
        gdf = gpd.read_file(gdf)
    elif not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError(f"Expected a GeoDataFrame or a file path, got {type(gdf)}")
    
    assert len(gdf) > 0, f"{FAIL} GeoDataFrame is empty"
    assert gdf.index.is_unique, f"{FAIL} Index is not unique"
    assert gdf.columns.is_unique, f"{FAIL} Columns are not unique"
    assert gdf.crs is not None, f"{FAIL} CRS is not set"
    assert gdf.is_valid.all(), f"{FAIL} Some geometries are invalid"
    # Note: gdf geometry does not have to be unique, as multiple points can have the same coordinates but different timestamps or depths.
    print(f"{PASS} GeoDataFrame is valid.")
    if show_info:
        print(gdf.crs)
        print(gdf.info())

    return True

#%% check DataFrame

# import pandas as pd
def check_df(df, show_info=False):
    """
    check a DataFrame by checking its type, index uniqueness, and column uniqueness.

    Parameters:
    df (pd.DataFrame or str): The DataFrame to check or the path to a file that can be read into a DataFrame.
    show_info (bool): Whether to print dataframe information.
    Returns: If the input is a file path, returns the loaded DataFrame; otherwise, returns None
    """
    if isinstance(df, str):
        df = pd.read_csv(df)
    elif not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected a DataFrame or a file path, got {type(df)}")
    
    assert len(df) > 0, f"{FAIL} DataFrame is empty"
    assert df.index.is_unique, f"{FAIL} Index is not unique"
    assert df.columns.is_unique, f"{FAIL} Columns are not unique"
    print(f"{PASS} DataFrame is valid.")
    if show_info:
        print(df.info())
    return True


#%% check 