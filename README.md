
Assumes data is already downloaded in GPX form in the `data/` directory:

```
data
└── gpx
    ├── CA_Sec_A_tracks.gpx
    ├── CA_Sec_A_waypoints.gpx
    ├── CA_Sec_B_tracks.gpx
    ├── CA_Sec_B_waypoints.gpx
...
```

Assumes `togeojson` is installed. Install with:
```
npm install -g @mapbox/togeojson
```

Set of waypoint symbols are:
```
{'Campground',
 'Car',
 'Cemetery',
 'Church',
 'CityCapitol',
 'DrinkingWater',
 'Flag',
 'FlagBlue',
 'FlagGreen',
 'FlagRed',
 'Forest',
 'GroundTransportation',
 'Lodge',
 'Lodging',
 'Park',
 'PicnicArea',
 'PostOffice',
 'Residence',
 'Restaurant',
 'Restroom',
 'ShoppingCenter',
 'SkiResort',
 'Summit',
 'TollBooth',
 'TrailHead',
 'TriangleRed',
 'Truck',
 'WaterHydrant',
 'WaterSource'}
```
