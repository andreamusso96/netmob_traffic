import itertools
import xarray as xr
import geopandas as gpd
import numpy as np
import pandas as pd
from datetime import time

import raster_utils

from .enums import City, TrafficDataDimensions
from .load import load_tile_geo_data_city


def rasterize_traffic_city_by_tile_service_time(traffic_data: xr.DataArray, city: City) -> xr.DataArray:
    traffic_tile_geo = load_tile_geo_data_city(city).to_crs(epsg=2154)
    traffic_tile_geo['geometry'] = traffic_tile_geo['geometry'].centroid

    service_raster = []
    for s in traffic_data[TrafficDataDimensions.SERVICE.value].values:
        traffic_service = traffic_data.sel(service=s).to_pandas()
        traffic_service = traffic_service.rename(columns={t:f'{t.strftime("%H:%M:%S")}' for t in traffic_data[TrafficDataDimensions.TIME.value].values})
        traffic_service_and_geo = gpd.GeoDataFrame(pd.merge(traffic_service, traffic_tile_geo, left_index=True, right_index=True))
        raster = raster_utils.rasterize_points(gdf=traffic_service_and_geo, measurements=list(traffic_service.columns), tile_size=100, no_data=np.nan, epsg=2154)
        raster = raster.rename({'variable': TrafficDataDimensions.TIME.value})
        raster = raster.assign_coords(service=s)
        service_raster.append(raster)

    city_raster = xr.concat(service_raster, dim=TrafficDataDimensions.SERVICE.value)
    return city_raster


def compute_zonal_statistics_traffic_raster(city: City, traffic_raster: xr.DataArray, vectors: gpd.GeoDataFrame, vector_id_col: str, coverage_threshold: float) -> pd.DataFrame:
    vectors = raster_utils.extract_vector_within_raster_coverage(raster=traffic_raster.isel(service=0, time=0), vector=vectors, coverage_threshold=coverage_threshold)
    iter_service_time = itertools.product(traffic_raster[TrafficDataDimensions.SERVICE.value].values, traffic_raster[TrafficDataDimensions.TIME.value].values)
    zonal_stats = [_get_zonal_statistics(c=city, s=s, t=t, raster=traffic_raster.sel(service=s, time=t), vectors=vectors, vector_id_col=vector_id_col) for s, t in iter_service_time]
    zonal_stats = pd.concat(zonal_stats)
    return zonal_stats


def _get_zonal_statistics(c: City, s: str, t: time, raster: xr.DataArray, vectors: gpd.GeoDataFrame, vector_id_col: str) -> pd.DataFrame:
    zonal_stats = raster_utils.extract_zonal_stats(raster=raster, no_data=np.nan, vector=vectors, stats=['mean'], all_touched=True)
    zonal_stats['service'] = s
    zonal_stats['time'] = t
    zonal_stats['city'] = c.value
    zonal_stats.rename(columns={'mean_raster_value': 'traffic'}, inplace=True)
    zonal_stats = zonal_stats[[vector_id_col, 'city', 'service', 'time', 'traffic']].copy()
    return zonal_stats
