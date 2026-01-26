#!/usr/bin/env bash

planner="arastar"

problem_number=${1:-"2"}

planning_space="manip" # manip and manip_dist allowed

dataset="$(rospack find bur_search_utils)/experiments/datasets/planar_7DoF"
roslaunch --wait smpl_test goal_planar_7dof_manip_vs_manip_dist.launch \
    problem_index:="${problem_number}" \
    dataset:="${dataset}" \
    planner:="${planner}" \
    planning_space:="${planning_space}" \
    epsilon:="50" \
    improve:="true" \
    visualize:="true"

planning_space="manip_dist"

roslaunch --wait smpl_test goal_planar_7dof_manip_vs_manip_dist.launch \
    problem_index:="${problem_number}" \
    dataset:="${dataset}" \
    planner:="${planner}" \
    planning_space:="${planning_space}" \
    improve:="true" \
    epsilon:="50" \
    visualize:="true"
