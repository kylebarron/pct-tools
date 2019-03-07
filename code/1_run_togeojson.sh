#! /usr/bin/env bash

data_dir=../data
mkdir -p $data_dir/geojson
for fname in $(ls $data_dir/gpx); do
    togeojson $data_dir/gpx/$fname \
        > $data_dir/geojson/$(basename -s .gpx $fname).geojson
done
