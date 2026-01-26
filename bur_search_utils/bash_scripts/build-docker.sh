#!/usr/bin/env bash

cd "$(dirname "$0")"/../.. || exit

if [[ "$(uname -s)" == "Darwin" ]]; then
    docker build -t bur_search_planning -f bur_search_utils/docker/Dockerfile .
else
    sudo docker build -t bur_search_planning -f bur_search_utils/docker/Dockerfile .
fi