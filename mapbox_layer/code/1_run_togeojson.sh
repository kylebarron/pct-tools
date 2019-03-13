#! /usr/bin/env bash

source_data_dir=../../data
data_dir=../data
mkdir -p $data_dir/geojson
for fname in $(ls $source_data_dir/gpx); do
    togeojson $source_data_dir/gpx/$fname \
        > $data_dir/geojson/$(basename -s .gpx $fname).geojson
done
