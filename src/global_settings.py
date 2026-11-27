# Define the root directory of the project
import os
import sys
from pathlib import Path
import datetime as dt
from figure_settings import *

print('Executing in:', sys.executable)
print('Current working directory:', os.getcwd())
print("Script run on:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


#%% ==== Functions and mappers ====
def find_project_root(path=None, marker="pyproject.toml"):
    if path is None:
        path = Path(__file__).resolve().parent
    if not isinstance(path, Path):
        path = Path(path)

    while not (path / marker).exists():
        if path.parent == path:
            raise FileNotFoundError(f"Cannot find {marker}")
        path = path.parent

    return path

dict_proj_crs = { # GDA94 / MGA zone 55/56
    'Amaroo': '28355',
    'Dinyah': '28355',
    'Llara': '28355',
    'Nowley': '28356',
    'Oodnadatta': '28356',
    'Willora': '28356',
}

# Set figure inset and legend locations based on farm name
dict_inset_loc = {
    'Amaroo': "upper left",
    'Dinyah': "upper right",
    'Llara': "lower left",
    'Nowley': "upper right",
    'Oodnadatta': "upper left",
}

dict_legend_loc = {
    'Amaroo': "lower left",
    'Dinyah': "lower left",
    'Llara': "lower right",
    'Nowley': "lower right",
    'Oodnadatta':"lower left",
}


#%% ==== Global Variables ====
# ROOT = find_project_root() # This may raise an error if the script is run from a different directory. Use the current working directory instead.
ROOT = find_project_root(path=os.getcwd(), marker="pyproject.toml")
print(f"Project root found at: {ROOT}")
BUFFER_DIS = 100    # m
GRID_SPACING = 100 # m

#%% ==== Class for Project Paths ====
class ProjectPaths():
    def __init__(self, farm_name):
        self.farm_name = farm_name
        self.root = ROOT

        self.raw = self.root / "data_raw" 
        self.raw_farm = self.raw / farm_name
        self.raw_file_nmdb = self.raw / "NMDB_JUNG_PreCorrE" / 'NMDB_JUNG_PreCorrE.csv'
        self.raw_file_rig = self.raw / "cutoff_rigidity.csv"

        self.lv1 = self.root / "data_lv1"
        self.lv1_farm = self.lv1 /farm_name

        self.lv1_shp = self.lv1_farm / "shapefiles"
        self.lv1_soil = self.lv1_farm / "soil"
        self.lv1_rover = self.lv1_farm / "rover"
        self.lv1_cov = self.lv1_farm / "covariates"

        self.lv2 = self.root/ "data_lv2"
        self.lv2_farm = self.lv2 / farm_name
        self.lv2_data = self.lv2_farm / "tabular_data"
        self.lv2_krig = self.lv2_farm / "kriging"
        self.lv2_ok = self.lv2_krig/ 'kriged_ok'
        self.lv2_b2pk = self.lv2_krig / 'kriged_b2pk'
        self.lv2_p2pk = self.lv2_krig / 'kriged_p2pk'

        self.lv2_cal = self.lv2_farm / "calibration"
        self.lv2_cal_b2pk = self.lv2_cal / "cal_b2pk"
        self.lv2_cal_p2pk = self.lv2_cal / "cal_p2pk"

        self.lv3 = self.root / "data_lv3"
        self.lv3_farm = self.lv3 / farm_name
        self.lv3_map = self.lv3_farm / "mapping"
        self.lv3_map_b2pk = self.lv3_map / "maps_b2pk"
        self.lv3_map_p2pk = self.lv3_map / "maps_p2pk"


        for dir_in in [self.raw]:
            assert dir_in.exists(), f"Directory {dir_in} does not exist. Please check the path."

        for dir_out in [self.lv1, self.lv1_shp, self.lv1_soil, self.lv1_rover, self.lv1_cov,
                        self.lv2, self.lv2_data,
                        self.lv2_krig, self.lv2_ok, self.lv2_b2pk, self.lv2_p2pk,
                        self.lv2_cal, # self.lv2_cal_b2pk, self.lv2_cal_p2pk,
                        self.lv3, self.lv3_farm,
                        self.lv3_map, self.lv3_map_b2pk, self.lv3_map_p2pk,
                        ]:
            dir_out.mkdir(parents=True, exist_ok=True)

        self.inset_loc = dict_inset_loc.get(farm_name, "upper right")
        self.legend_loc = dict_legend_loc.get(farm_name, "upper right")
        self.proj_crs = dict_proj_crs.get(farm_name, "28355")  # Default to GDA94 / MGA zone 55 if farm not found

        print(f"Project paths initialized for farm: {farm_name}")


if __name__ == "__main__":
        
    # Default farm name, can be changed as needed
    FARM_NAME = os.environ.get("FARM_NAME", "Amaroo")
    dirs = ProjectPaths(farm_name=FARM_NAME)