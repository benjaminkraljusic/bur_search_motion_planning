#!/usr/bin/env bash

planner="arastar"

# available planners:
# "arastar"
# "awastar"
# "mhastar"
# "larastar"
# "egwastar"
# "padastar"

problem_number=1

dataset="$(rospack find smpl_test)/2DoF_planar/planar_7dof_datasets"
roslaunch --wait smpl_test goal_planar_7dof_bur_planning.launch \
    problem_index:="${problem_number}" \
    dataset:="${dataset}" \
    planner:="${planner}" \
    visualize:="true" & 
wait


