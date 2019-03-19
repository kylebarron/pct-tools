import re
import json
from pathlib import Path


def main():
    data_dir = Path('../data/geojson')
    merge_waypoints(data_dir)
    merge_tracks(data_dir)


def merge_waypoints(data_dir):
    paths = [x for x in data_dir.iterdir() if x.stem.endswith('waypoints')]
    paths = sorted(paths)

    merged = {'type': 'FeatureCollection', 'features': []}
    for path in paths:
        with path.open() as f:
            d = json.load(f)

        merged['features'].extend(d['features'])

    for feature in merged['features']:
        sym = feature['properties']['sym']
        sym_short = re.sub(r'[^\w]', '', sym)
        feature['properties']['sym'] = sym_short

    for feature in merged['features']:
        desc = feature['properties'].get('desc')
        if not desc:
            continue
        if not re.search(r'WATER ALERT', desc):
            continue
        feature['properties']['sym'] = 'WaterSourceAlert'

    print('The set of features needed to color are:')
    print(set([x['properties']['sym'] for x in merged['features']]))

    with open('../data/final_waypoints.geojson', 'w') as f:
        json.dump(merged, f)


def merge_tracks(data_dir):
    paths = [x for x in data_dir.iterdir() if x.stem.endswith('tracks')]
    paths = sorted(paths)

    merged = {'type': 'FeatureCollection', 'features': []}
    for path in paths:
        with path.open() as f:
            d = json.load(f)

        merged['features'].extend(d['features'])

    for feature in merged['features']:
        main_trail = re.search(
            r'^(CA|OR|WA) Sec [A-Z]$', feature['properties']['name'])
        feature['properties']['main_trail'] = bool(main_trail)

    with open('../data/final_tracks.geojson', 'w') as f:
        json.dump(merged, f)


if __name__ == '__main__':
    main()
