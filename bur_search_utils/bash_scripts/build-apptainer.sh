#!/usr/bin/env bash

user_specified_path="$1"
container_path="${user_specified_path:-"${HOME}"/bur_search_apptainer}"
ws_path="$(dirname "$(realpath "$0")")"/../../../..

if [[ ! -f "${container_path}"/singularity ]]; then
    apptainer build \
        --bind "${ws_path}":/opt/catkin_ws \
        --sandbox "${container_path}" \
        "${ws_path}"/src/bur_search_motion_planning/bur_search_utils/apptainer/bur_search_planning.def
else
    apptainer exec \
        --writable "${container_path}" \
        "${ws_path}"/src/bur_search_motion_planning/bur_search_utils/bash_scripts/build-ws.sh
fi
