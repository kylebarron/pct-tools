#! /usr/bin/env bash

wget \
    --timestamping \
    --no-remove-listing \
    --convert-links \
    --adjust-extension \
    --page-requisites \
    --no-parent \
    --load-cookies cookies.txt \
    -D hikerbeta.com,squarespace.com,patreon.com,typekit.net \
    --span-hosts \
    --mirror \
    --random-wait \
    --wait=1 \
    https://hikerbeta.com/
