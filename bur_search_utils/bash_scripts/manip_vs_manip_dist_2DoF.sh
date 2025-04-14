#!/usr/bin/env bash

planner="arastar"

planning_space="manip" # manip and manip_dist allowed

problem_number=$1

dataset="$(rospack find smpl_test)/planar_arm/planar_2dof_datasets"
roslaunch --wait smpl_test goal_planar_2dof_manip_vs_manip_dist.launch \
    problem_index:="${problem_number}" \
    dataset:="${dataset}" \
    planner:="${planner}" \
    planning_space:="${planning_space}" \
    epsilon:="100" \
    improve:="true" \
    visualize:="true"

# Copy contents from temporary file to the final destination and remove the temporary file
cp ~/.ros/manipTmp.txt $(rospack find bur_search_utils)/2D_search_nodes/manip.txt
rm ~/.ros/manipTmp.txt

planning_space="manip_dist"

roslaunch --wait smpl_test goal_planar_2dof_manip_vs_manip_dist.launch \
    problem_index:="${problem_number}" \
    dataset:="${dataset}" \
    planner:="${planner}" \
    planning_space:="${planning_space}" \
    epsilon:="100" \
    improve:="true" \
    visualize:="true"  

# Copy contents from temporary file to the final destination and remove the temporary file
cp ~/.ros/manip_dist.txt $(rospack find bur_search_utils)/2D_search_nodes/manip_dist.txt
rm ~/.ros/manip_dist.txt

python3 $(rospack find bur_search_utils)/python_scripts/plot_search.py $1	
