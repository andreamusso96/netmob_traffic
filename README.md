## Netmob traffic data

This package has essentially two main goals. First, abstract away the process of loading the netmob traffic data into an xarray object. 
Second, provide enums for the different dimensions of the netmob traffic data.

In order to use the package you need to specify the path to the netmob traffic data. 
This can be done as follows
```python
import netmob_traffic as nt
nt.initialize_data_directory('/path/to/data')
```
## Enums
The package contains various enums to facilitate life when dealing with the data the most important ones are
```python
nt.City # Enum for the different cities in the data
nt.TrafficType # Enum for the different traffic types in the data (Uplink, Downlink, Both)
nt.Service # Enum for the different services in the data
```
The ```TimeOptions``` class contains method ```get_days``` and ```get_times``` that can be used to get the days for which data is available.

## Loading data
You can load the data for paris for both uplink and downlink traffic for the services facebook and youtube for all days as follows:
```python
import netmob_traffic as nt
data = nt.load_traffic_data_city(city=nt.City.PARIS, traffic_type=nt.TrafficType.UL_AND_DL, service=[nt.Service.FACEBOOK, nt.Service.YOUTUBE], day=nt.TimeOptions.get_days())
```
You can load the tile geojon data in a similar fashion
```python
nt.load_tile_geojon_data_city(city=nt.City.PARIS)
```
