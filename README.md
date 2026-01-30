# Bur Search Motion Planning
 Motion planning for robotic manipulators that combines sampling-based and search-based planning methods. Distance-based burs[^1] of free configuration space (C-space) are used as adaptive motion primitives within the graph search algorithm. The algorithm is implemented within the existing SMPL (Search-Based Motion Planning Library) library.

 :page_facing_up: Paper: [Search-Based Robot Motion Planning With Distance-Based Adaptive Motion Primitives](https://arxiv.org/abs/2507.01198)

 [^1] Lacevic, Bakir, et al. Burs of Free C-Space: A Novel Structure for Path Planning. 05 2016, pp. 70–76, https://doi.org/10.1109/ICRA.2016.7487117.

## :rewind: Prerequisites
Docker is required and can be installed from this [link](https://docs.docker.com/get-started/get-docker/).
## :hammer_and_wrench: Build
1. Clone this repository recursively and navigate to the right directory:
    ```bash
    git clone --recurse-submodules https://github.com/benjaminkraljusic/bur_search_motion_planning.git && cd 
    bur_search_motion_planning
    ```
2. Call the Docker image building script:
    ```bash
    ./bur_search_utils/bash_scripts/build-docker.sh
    ```
    Done.
## :running: Running
In the terminal, from the cloned directory that was previously navigated to, run:
```bash
./bur_search_utils/bash_scripts/run-docker.sh
```
The Docker container is now running with the terminal attached. The commands in the following sections should be run in the same terminal, unless stated otherwise.
## :computer: Usage
The project can be used as:
- A development environment for search-based robot motion planning using SMPL and/or burs of free C-space.
- A framework for comparing classical motion-primitive planning with the proposed approach using burs of free C-space as adaptive motion primitives.
### :gear: Development environment
The directory containing the source code is mounted as a volume inside the Docker container, which means that any changes made in the cloned directory on the host machine are reflected in the container as well. As a result, it is not necessary to rebuild the Docker image every time the source code changes.

The project uses standard [catkin workspace](https://wiki.ros.org/catkin/workspaces) structure. To navigate to the workspace directory, run:
```bash
cd /ws
```
To build the code, run the following command inside the workspace:
```bash
catkin build
```
### :arrow_forward: Running examples

## :link: Links

