# Read file and skip rows starting with '//'
import pandas as pd
import numpy as np
import pandas as pd
import warnings
# Suppress only the SettingWithCopyWarning
# warnings.filterwarnings("ignore", category=FutureWarning, message=".*numeric_only.*")


#########################################################
# %% Rover Data Processing and Quality Control
#########################################################
def parse_rover(filepth):
        """Parse rover raw data file and return a pandas DataFrame.
        Args:
            filepth (str): The path to the rover data file.
        Returns:
            pandas.DataFrame: The parsed rover data.
        """
        

        infos = []
        rows = []
        headers = []
        switch = False
        with open(filepth, mode='r') as f:
            for line in f:
                if line.lstrip().startswith("//"): # skip comment rows (trim leading spaces first)
                    infos.append(line.rstrip("\n"))
                    if switch:
                        headers.append(line.rstrip("\n").strip("//"))
                    if line.lstrip().startswith("//--Data Column Info"):
                        switch = True
                else:
                    switch = False
                    row = line.rstrip("\n")
                    if row != '':
                        row = [i.strip(' ') for i in row.split(',')]
                        rows.append(row)

        headers = ''.join(headers)
        headers = [i.strip(' ') for i in headers.split(',')]
        if(len(rows) > 0) & (headers !=['']):
            df = pd.DataFrame(rows, columns=headers)
            # Drop duplicated rows
            df = df.drop_duplicates(subset=['Date Time(UTC)'])
            # Drop duplicated columns
            df = df.loc[:, ~df.columns.duplicated()]
            return df


def qc_rover(df):
    """Perform quality control on rover data file.
    Args:
        df (pandas.DataFrame): The rover data to be checked.
    Returns:
        df (pandas.DataFrame): The rover data after quality control.
        dict: A dictionary containing the quality control results.
    """
    if df is None:
        print("No data found in the rover file.")
        return False, {}

    # Check for missing values
    if df.isnull().values.any():
        print("Missing values found in the rover data.")
        return False, {"missing_values": True}

    # Check for duplicate rows
    if df.duplicated().any():
        print("Duplicate rows found in the rover data.")
        return False, {"duplicate_rows": True}

    # Check for duplicate columns
    if df.columns.duplicated().any():
        print("Duplicate columns found in the rover data.")
        return False, {"duplicate_columns": True}

    print("Rover data quality control passed.")
    return True, {}



#%% Resample soil depth internals
#  Functions (resample) to resample soil depth intervals.

def resample(df_sub, depth_new=[0, 10, 30, 60, 80, 100], increment=5):
    # Define the new depth intervals
    site_id = df_sub['SiteID'].unique()[0]
    date = df_sub['Date'].unique()[0]
    idx_num = [i for i, v in enumerate(df_sub.dtypes) if v is not np.dtype('O')]
    df_sub.sort_values(['DepthUpper', 'DepthLower'], inplace=True)

    ### Create a dataframe of all depth increments (e.g., 5cm)
    # Create an empty row
    row_empty = df_sub.iloc[0].copy()
    row_empty.iloc[idx_num] = np.nan
    row_empty['SiteID'] = site_id
    row_empty['Date'] = date
    if 'Longitude' in df_sub.columns and 'Latitude' in df_sub.columns:
        row_empty['Longitude'] = df_sub.iloc[0]['Longitude']
        row_empty['Latitude'] = df_sub.iloc[0]['Latitude']
    # print ('Empty row is', row_empty)

    ### Create a list of small depth intervals
    depth_min = min(df_sub['DepthUpper'].min(), depth_new[0])
    depth_max = max(df_sub['DepthLower'].max(), depth_new[-1])
    depth_increments = np.arange(depth_min, depth_max+increment, increment)
    # Create a new empty frame with depth top and depth bottom
    df_fill = pd.DataFrame({'DepthUpper': depth_increments[:-1], 'DepthLower': depth_increments[1:]})

    ### Break original dataframe into intervals
    df_increment = []
    for idx, row in df_sub.iterrows():
        depth_top = row['DepthUpper']
        depth_bot = depth_top + increment
        while depth_bot <= row['DepthLower']:
            row2 = row.copy()
            row2['DepthUpper'] = depth_top
            row2['DepthLower'] = depth_bot
            depth_top = depth_bot
            depth_bot = depth_top + increment
            df_increment.append(row2)
    df_increment = pd.concat(df_increment, axis=1).T
    # print('Debuging...df_increment is', df_increment)
    
    ### Merge with the new depth increments to fill in missing intervals with NaN
    df_increment = df_fill.merge(df_increment, on=['DepthUpper', 'DepthLower'], how='left')

    # Fillna with interpolation for numeric values or forward/backward fill for non-numeric values
    for col in df_increment.columns:
        try:
            df_increment[col] = df_increment[col].astype(float).interpolate(method='linear', limit_direction='both')
        except ValueError:
            df_increment[col] = df_increment[col].fillna(method='ffill').fillna(method='bfill')
            # print(f"Column {col} cannot be converted to float.")

    df_increment = df_increment.astype(df_sub.dtypes)

    ### Average values within the target depth intervals

    idx_num = [i for i, v in enumerate(df_increment.dtypes) if v is not np.dtype('O')]
    idx_obj = [i for i, v in enumerate(df_increment.dtypes) if v is np.dtype('O')]
    if 'Longitude' in df_increment.columns:
        idx_num.remove(df_increment.columns.get_loc('Longitude'))
        idx_obj.append(df_increment.columns.get_loc('Longitude'))
    if 'Latitude' in df_increment.columns:
        idx_num.remove(df_increment.columns.get_loc('Latitude'))
        idx_obj.append(df_increment.columns.get_loc('Latitude'))

    df_mean = []
    for bot, top in zip(depth_new[1:], depth_new[:-1]):
        df_increment_sub = df_increment.loc[(df_increment['DepthUpper'] >= top) & (df_increment['DepthLower'] <= bot), :]

        if df_increment_sub.empty:
            row_empty2 = row_empty.copy()
            row_empty2['DepthUpper'] = top
            row_empty2['DepthLower'] = bot
            df_mean.append(row_empty2)

        else:
            interval_mean = df_increment_sub[df_increment_sub.columns[idx_num]].mean() #.map(lambda x: np.round(x, 3)) # Dont round here, it changes coordinates.
            # print('df3sub', df3_mean)
            text = df_increment_sub[df_increment.columns[idx_obj]].mode()
            # print('Debuging...', text)
            interval_mean = pd.concat([interval_mean, text.iloc[0, :]])
            interval_mean['DepthUpper'] = top
            interval_mean['DepthLower'] = bot
            # print(df3_mean)
            df_mean.append(interval_mean)

    df_mean = pd.concat(df_mean, axis=1).T
    df_mean = df_mean.astype(df_sub.dtypes) .sort_values(['SiteID', 'DepthUpper', 'DepthLower'])
    return df_mean


def batch_resample(df, depth_new):
    dfs_new = []
    if 'Date' not in df.columns:
        df['Date'] = 'unspecified'

    for site_id in df['SiteID'].unique():
        for date in df['Date'].unique():
            df_sub = df[(df['SiteID'] == site_id) & (df['Date']==date)].sort_values(['DepthLower', 'DepthUpper'])
            if len(df_sub) == 0:
                continue
            # try:
            if True:
                df_new = resample(df_sub, depth_new=depth_new)
                # print(df_new)
                dfs_new.append(df_new)
                # print(site_id, date, '===============')
                # print(df_new)
            # except:
            #     print(df_sub[['DepthUpper', 'DepthLower']])
            #     print('====')
        # break
    dfs_new = pd.concat(dfs_new)
    return dfs_new



#%% Extract raster values at specified points.
def extract_raster_values(points, raster, tolerance=None):
    """
    Extract values from a raster at specified points.
    Parameters:
    - points: geometry points (e.g., shapely Points or GeoPandas GeoSeries) where values need to be extracted.
    - raster: An xarray DataArray representing the raster data.
    - tolerance: The maximum distance to consider when extracting values.
    Returns:
    - A numpy array of values extracted from the raster at the specified points.
    """
    if tolerance is None:
        x_res = np.abs(raster["x"].diff("x")).median().item()
        y_res = np.abs(raster["y"].diff("y")).median().item()
        tolerance = max(x_res, y_res) * 1.5

    values = []
    for point in points:
        value = raster.sel(x=point.x, y=point.y, method='nearest', tolerance=tolerance).values
        values.append(value)
    return np.array(values)

