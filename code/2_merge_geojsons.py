import re
import json
from pathlib import Path

data_dir = Path('../data/geojson')
paths = [x for x in data_dir.iterdir() if not x.stem.endswith('tracks')]
paths = sorted(paths)

merged = {'type': 'FeatureCollection', 'features': []}
for path in paths:
    with path.open() as f:
        d = json.load(f)

    merged['features'].extend(d['features'])

for feature in merged['features']:
    feature['properties']['sym'] = re.sub(r'[^\w]', '', feature['properties']['sym'])

print('The set of features needed to color are:')
set([x['properties']['sym'] for x in merged['features']])

with open('../data/final.geojson', 'w') as f:
    json.dump(merged, f)
