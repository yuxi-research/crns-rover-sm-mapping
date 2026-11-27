
try:
    import global_settings
    import utils.check_data
    print("Project modules installed successfully.")

except ImportError as e:
    print(f"Error importing project modules: {e}")
    print('Please run "uv pip install -e ."" to install the project modules.')

import geopandas
import pandas
import matplotlib
import notebook
import papermill
import pyinterpolate
import pykrige
import rasterio
import rioxarray
import seaborn
import xarray

print("All packages are installed and imported successfully.")

print("All tests passed successfully.")