#!/usr/bin/env bash

planner="arastar"

planning_space="manip" # manip and manip_dist allowed

problem_number=1

dataset="$(rospack find smpl_test)/planar_arm/planar_2dof_datasets"
roslaunch --wait smpl_test goal_planar_2dof_manip_vs_manip_dist.launch \
    problem_index:="${problem_number}" \
    dataset:="${dataset}" \
    planner:="${planner}" \
    planning_space:="${planning_space}" \
    visualize:="true"

cp ~/TezaETF/code/dok_ne_skontam_sto/manipulacija.txt ~/TezaETF/code/dok_ne_skontam_sto/manip.txt

planning_space="manip_dist"

roslaunch --wait smpl_test goal_planar_2dof_manip_vs_manip_dist.launch \
    problem_index:="${problem_number}" \
    dataset:="${dataset}" \
    planner:="${planner}" \
    planning_space:="${planning_space}" \
    visualize:="true" & 
wait
