#!/usr/bin/env bash
planner="arastar"

dataset="$(rospack find bur_search_utils)/experiments/datasets/planar_7DoF"

# Chose the scene
for problem_number in 1 2 3
do
    # Chose motion primitive length
    for m_prim_len in 5 6 7 8 9 10 11 12
    do
        m_prim_file="$(rospack find bur_search_utils)/experiments/datasets/planar_7DoF/m_prim_files/planar_7dof_"$m_prim_len".mprim"

        # Create planning stats files for the scene
        MANIP_LOG_FILE="$(rospack find bur_search_utils)/experiments/results/planar_7DoF/scene000"$problem_number/"manip-"$m_prim_len".csv"
        MANIP_DIST_LOG_FILE="$(rospack find bur_search_utils)/experiments/results/planar_7DoF/scene000"$problem_number/"manip_dist-"$m_prim_len".csv"

        # add header
        HEADER="exp_init,exp_final,time_init,time_final,eps_final,path_len"

        echo "$HEADER" > "$MANIP_LOG_FILE"
        echo "$HEADER" > "$MANIP_DIST_LOG_FILE"
        
        # Execute the experiment 100 times
        for (( experiment_number=1; experiment_number<=100; experiment_number++ ))
        do
            planning_space="manip" # manip and manip_dist allowed

            roslaunch --wait smpl_test goal_planar_7dof_manip_vs_manip_dist.launch \
                problem_index:="${problem_number}" \
                dataset:="${dataset}" \
                planner:="${planner}" \
                planning_space:="${planning_space}" \
                epsilon:="50" \
                improve:="true" \
                m_prim_file:="${m_prim_file}" \
                stats_file:="${MANIP_LOG_FILE}"

            planning_space="manip_dist"

            roslaunch --wait smpl_test goal_planar_7dof_manip_vs_manip_dist.launch \
                problem_index:="${problem_number}" \
                dataset:="${dataset}" \
                planner:="${planner}" \
                planning_space:="${planning_space}" \
                epsilon:="50" \
                improve:="true" \
                m_prim_file:="${m_prim_file}" \
                stats_file:="${MANIP_DIST_LOG_FILE}"
        done

    done
done
