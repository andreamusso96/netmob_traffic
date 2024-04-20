# Netmob traffic data

This package provide basic infrastructure to work with the netmob traffic dataset.
This dataset was released as part of the [NetMob Data Challenge 2023](https://netmob2023challenge.networks.imdea.org/) 

The package contains essentially two scripts:
1. The first script abstract away the process of loading the netmob traffic data into and xarray object. 
2. The second script provides enumerations (Enum) for the different dimensions of the netmob traffic data.

## Installation

To install the package just clone the repostiory on your computer running
```bash
git clone https://github.com/andreamusso96/netmob_traffic.git
```

Then navigate to the directory and run
```bash
pip install -e .
```
The -e flag is used to install the package in editable mode, so that you can modify the code and see the changes without having to reinstall the package.
If you do not want to edit the package you can just remove the -e flag.


## Usage
### Initialization
In order to use the package you need to specify the path to the netmob traffic data. 
This can be done as follows
```python
import netmob_traffic as nt
nt.initialize_data_directory('/path/to/data')
```
### Enums
The package contains various enums to facilitate life when dealing with the data. 
The most important ones are
```python
nt.City # Enum for the different cities in the data
nt.TrafficType # Enum for the different traffic types in the data (Uplink, Downlink, Both)
nt.Service # Enum for the different services in the data
```
On top of these enums the ```TimeOptions``` class contains method ```get_days``` and ```get_times``` that can be used to get the days and times for which data is available.

### Loading data
You can load the data for paris for both uplink and downlink traffic for the services facebook and youtube for all days as follows:
```python
import netmob_traffic as nt
data = nt.load_traffic_data_city(city=nt.City.PARIS, traffic_type=nt.TrafficType.UL_AND_DL, service=[nt.Service.FACEBOOK, nt.Service.YOUTUBE], day=nt.TimeOptions.get_days())
```
You can load the tile geojon data in a similar fashion
```python
nt.load_tile_geojon_data_city(city=nt.City.PARIS)
```
