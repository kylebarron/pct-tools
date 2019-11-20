#! /usr/bin/env bash

wget \
    --timestamping \
    --no-remove-listing \
    --convert-links \
    --adjust-extension \
    --page-requisites \
    --no-parent \
    -D andrewskurka.com,bootstrapcdn.com,netdna-ssl.com,optmnstr.com,gravatar.com,typekit.com \
    --span-hosts \
    --mirror \
    --random-wait \
    --wait=0.1 \
    https://andrewskurka.com/
