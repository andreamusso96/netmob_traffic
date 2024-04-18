from typing import List

import numpy as np
import xarray as xr
from datetime import time, datetime, timedelta

from .enums import TrafficDataDimensions, TrafficType, City, Service, TimeOptions
from .load import load_traffic_data_city
from .clean import remove_times_outside_range, remove_nights_before_holidays, remove_nights_before_anomalies


def get_night_traffic_city_by_tile_service_time(city: City, traffic_type: TrafficType, start_night: time, end_night: time, service: List[Service], remove_nights_before_holiday_and_anomalies: bool = True):
    traffic_data_city = []
    for i in range(0, len(service), 5):
        service_ = service[i:i + 5]
        traffic_data_service = load_traffic_data_city(traffic_type=traffic_type, city=city, service=service_, day=TimeOptions.get_days())
        traffic_data_service = day_time_to_datetime_index(xar=traffic_data_service)
        if remove_nights_before_holiday_and_anomalies:
            traffic_data_service = remove_nights_before_holidays(traffic_data=traffic_data_service)
            traffic_data_service = remove_nights_before_anomalies(traffic_data=traffic_data_service, city=city)

        traffic_data_service = remove_times_outside_range(traffic_data=traffic_data_service, start=start_night, end=end_night)
        traffic_data_service = traffic_data_service.groupby(group=f'{TrafficDataDimensions.DATETIME.value}.time').sum()
        sorted_time_index = _sort_time_index(time_index=traffic_data_service.time.values, reference_time=start_night)
        traffic_data_service = traffic_data_service.reindex({TrafficDataDimensions.TIME.value: sorted_time_index})
        traffic_data_city.append(traffic_data_service)

    traffic_data_city = xr.concat(traffic_data_city, dim=TrafficDataDimensions.SERVICE.value)
    return traffic_data_city


def day_time_to_datetime_index(xar: xr.DataArray) -> xr.DataArray:
    new_index = np.add.outer(xar.indexes[TrafficDataDimensions.DAY.value], xar.indexes[TrafficDataDimensions.TIME.value]).flatten()
    datetime_xar = xar.stack(datetime=(TrafficDataDimensions.DAY.value, TrafficDataDimensions.TIME.value), create_index=False)
    datetime_xar = datetime_xar.reindex({TrafficDataDimensions.DATETIME.value: new_index})
    return datetime_xar


def _sort_time_index(time_index: List[time], reference_time: time):
    auxiliary_day = datetime(2020, 2, 1)
    auxiliary_dates = []

    for t in time_index:
        if t < reference_time:
            auxiliary_dates.append(datetime.combine(date=auxiliary_day + timedelta(days=1), time=t))
        else:
            auxiliary_dates.append(datetime.combine(date=auxiliary_day, time=t))

    auxiliary_dates.sort()
    sorted_times = [d.time() for d in auxiliary_dates]
    return sorted_times
