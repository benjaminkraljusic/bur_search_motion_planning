#!/usr/bin/env bash

planner="arastar"

# planner MOZE BITI:
# "arastar"
# "awastar"
# "mhastar"
# "larastar"
# "egwastar"
# "padastar"

problem_number=1

dataset="$(rospack find smpl_test)/2DoF_planar/planar_2dof_datasets"
roslaunch --wait smpl_test goal_planar_2dof_bur_planning.launch \
    problem_index:="${problem_number}" \
    dataset:="${dataset}" \
    planner:="${planner}" \
    visualize:="true" \
    verbose:="true" & 
wait


