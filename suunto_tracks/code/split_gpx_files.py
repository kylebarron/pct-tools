#! /usr/bin/env python3
"""
Clip Halfmile Tracks into sections of 1000 points each for use with Suunto Ambit
3 Peak without losing accuracy
"""

import re
import math
import gpxpy
import gpxpy.gpx

from pathlib import Path


def main():

    data_dir = Path('../../data/gpx/')
    out_dir = Path('../data/')
    out_dir.mkdir(exist_ok=True, parents=True)

    sections = {
        'ca_south': [
            'CA_Sec_A', 'CA_Sec_B', 'CA_Sec_C', 'CA_Sec_D', 'CA_Sec_E',
            'CA_Sec_F', 'CA_Sec_G'],
        'ca_central': [
            'CA_Sec_H', 'CA_Sec_I', 'CA_Sec_J', 'CA_Sec_K', 'CA_Sec_L',
            'CA_Sec_M'],
        'ca_north': [
            'CA_Sec_N',
            'CA_Sec_O',
            'CA_Sec_P',
            'CA_Sec_Q',
            'CA_Sec_R', ],
        'or': [
            'OR_Sec_B', 'OR_Sec_C', 'OR_Sec_D', 'OR_Sec_E', 'OR_Sec_F',
            'OR_Sec_G'],
        'wa': ['WA_Sec_H', 'WA_Sec_I', 'WA_Sec_J', 'WA_Sec_K', 'WA_Sec_L']}

    for name, stubs in sections.items():
        track_paths = [data_dir / f'{x}_tracks.gpx' for x in stubs]
        main, alt = combine_tracks(track_paths)
        main_tracks = split_main_track(main)
        (out_dir / name).mkdir(parents=True, exist_ok=True)
        (out_dir / name / 'alt').mkdir(parents=True, exist_ok=True)

        i = 0
        for track in main_tracks:
            i += 1
            new_gpx = gpxpy.gpx.GPX()
            new_gpx.tracks.append(track)

            fname = f'{name}_{i}_trk.gpx'
            with open(out_dir / name / fname, 'w') as f:
                f.write(new_gpx.to_xml())

        for track in alt:
            new_gpx = gpxpy.gpx.GPX()
            new_gpx.tracks.append(track)
            fname = f'{track.name}.gpx'
            with open(out_dir / name / 'alt' / fname, 'w') as f:
                f.write(new_gpx.to_xml())


def combine_tracks(track_paths):
    """Combine all main tracks for each state into
    """
    track_paths = sorted(track_paths)

    main_track = gpxpy.gpx.GPXTrack()
    main_segment = gpxpy.gpx.GPXTrackSegment()

    alt_tracks = []

    for track_path in track_paths:
        with open(track_path) as f:
            gpx = gpxpy.parse(f)

        for track in gpx.tracks:
            main_trail = re.search(r'^(CA|OR|WA) Sec [A-Z]$', track.name)
            if main_trail:
                assert len(track.segments) == 1
                segment = track.segments[0]
                main_segment.points.extend(segment.points)
            else:
                alt_tracks.append(track)

    main_track.segments.append(main_segment)
    return main_track, alt_tracks


def split_main_track(track):
    new_tracks = []

    assert len(track.segments) == 1
    segment = track.segments[0]
    points = segment.points.copy()

    n_tracks = math.ceil(len(segment.points) / 1000)
    points_per_track = math.ceil(len(segment.points) / n_tracks)

    for i in range(n_tracks):
        new_track = gpxpy.gpx.GPXTrack()
        new_segment = gpxpy.gpx.GPXTrackSegment()

        start_pt = i * points_per_track
        end_pt = (i + 1) * points_per_track
        new_segment.points.extend(points[start_pt:end_pt])
        new_track.segments.append(new_segment)
        new_tracks.append(new_track)

    return new_tracks


if __name__ == '__main__':
    main()
