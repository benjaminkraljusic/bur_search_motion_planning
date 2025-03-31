#!/usr/bin/env bash

planner="arastar"

problem_number=$1

planning_space="manip" # manip and manip_dist allowed

dataset="$(rospack find smpl_test)/planar_arm/planar_7dof_datasets"
roslaunch --wait smpl_test goal_planar_7dof_manip_vs_manip_dist.launch \
    problem_index:="${problem_number}" \
    dataset:="${dataset}" \
    planner:="${planner}" \
    planning_space:="${planning_space}" \
    visualize:="true"

planning_space="manip_dist"

roslaunch --wait smpl_test goal_planar_7dof_manip_vs_manip_dist.launch \
    problem_index:="${problem_number}" \
    dataset:="${dataset}" \
    planner:="${planner}" \
    planning_space:="${planning_space}" \
    visualize:="true" & 
wait
