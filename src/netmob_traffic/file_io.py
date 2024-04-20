import os
from datetime import date

import xarray as xr

from .enums import City, Service, TrafficType

data_dir = None


def initialize_data_directory(folder: str):
    global data_dir
    data_dir = folder
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f'Data directory {data_dir} does not exist')


def get_mobile_traffic_data_file_path(traffic_type: TrafficType, city: City, service: Service, day: date):
    assert data_dir is not None, 'Data directory not initialized, call initialize_data_directory before using this function'
    day_str = day.strftime('%Y%m%d')
    path = f'{data_dir}/tile/{city.value}/{service.value}/{day_str}/'
    file_name = f'{city.value}_{service.value}_{day_str}_{traffic_type.value}.txt'
    file_path = path + file_name
    return file_path


def get_geo_data_file_path(city: City) -> str:
    assert data_dir is not None, 'Data directory not initialized, call initialize_data_directory before using this function'
    return f'{data_dir}/{city.value}.geojson'


def save_mobile_traffic_data_by_tile_service_time(city: City, data: xr.DataArray, folder_path: str):
    time_as_str = [str(t) for t in data.time.values]
    data_ = data.assign_coords(time=time_as_str)
    data_.to_netcdf(f'{folder_path}/traffic_{city.value.lower()}_by_tile_service_time.nc')
