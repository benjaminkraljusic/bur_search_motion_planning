import matplotlib.pyplot as plt
import re
import math
import yaml
import numpy as np
import sys

# Constants
RESOLUTION = 0.017453292519943295  # 1 degree in radians
CIRCLE_RADIUS = 0.05              # Each robot circle has radius 0.05

###############################
# Parsing Functions
###############################

def parse_search_file(filename):
    """
    Parse a planning file for states, edges, and (optionally) a solution path.
    
    - Lines starting with "P:" indicate a parent state.
    - Lines starting with "K" indicate a child state connected to the last parent.
    - Lines starting with "G:" indicate goal states.
    - After a line that begins with "SOLUTION:" all lines starting with '[' are considered part of the solution.
    
    Returns a tuple (edges, nodes, solution) where:
      - edges is a list of (parent, child) pairs,
      - nodes is a set of states,
      - solution is a list of states (in order) if found, otherwise an empty list.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    edges = []
    nodes = set()
    solution = []
    parent = None
    in_solution = False
    for line in lines:
        line = line.strip()
        if line.startswith("SOLUTION:"):
            in_solution = True
            continue
        if in_solution:
            # Look for lines that start with '[' to parse a solution state.
            if line.startswith('[') and line.endswith(']'):
                # Extract numbers from the line.
                nums = list(map(float, re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", line)))
                if len(nums) == 2:
                    solution.append(tuple(nums))
            continue
        if not (line.startswith("P:") or line.startswith("G:") or line.startswith("K")):
            continue
        coords = list(map(float, re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", line)))
        if len(coords) != 2:
            continue
        if line.startswith("P:"):
            parent = tuple(coords)
            nodes.add(parent)
        elif line.startswith("K"):
            if parent is not None:
                child = tuple(coords)
                edges.append((parent, child))
                nodes.add(child)
        elif line.startswith("G:"):
            nodes.add(tuple(coords))
    return edges, nodes, solution

def parse_scene_yaml(scene_file):
    """Parse the scene YAML file."""
    with open(scene_file, 'r') as f:
        scene = yaml.safe_load(f)
    return scene

def get_obstacles(scene):
    """
    Extract obstacles from the scene YAML.
    For each collision object (box or sphere), return a dict with its 2D geometry.
    """
    obstacles = []
    world = scene.get("world", {})
    collision_objects = world.get("collision_objects", [])
    for obj in collision_objects:
        primitives = obj.get("primitives", [])
        poses = obj.get("primitive_poses", [])
        for prim, pose in zip(primitives, poses):
            pos = pose.get("position", [0,0,0])
            x, y = pos[0], pos[1]
            if prim.get("type") == "box":
                dims = prim.get("dimensions", [0,0,0])
                obstacles.append({
                    "type": "box",
                    "center": (x, y),
                    "width": dims[0],
                    "height": dims[1]
                })
            elif prim.get("type") == "sphere":
                dims = prim.get("dimensions", [0])
                obstacles.append({
                    "type": "sphere",
                    "center": (x, y),
                    "radius": dims[0]
                })
    return obstacles

###############################
# Robot Kinematics (Circle Model, Swapped Coordinates)
###############################

def rotate_point(p, theta):
    """
    Rotate a point p = (x,y) by angle theta using the standard rotation:
    (x*cosθ - y*sinθ, x*sinθ + y*cosθ)
    """
    x, y = p
    return (x * math.cos(theta) - y * math.sin(theta),
            x * math.sin(theta) + y * math.cos(theta))

def robot_circle_centers(theta1, theta2):
    """
    Compute the world coordinates of all circles representing the robot.
    For Link1, local centers are defined as (d, 0) for d in [0, 0.05, 0.10, 0.15, 0.20].
    For Link2, the local centers are similarly (d, 0) for d in [0, 0.05, 0.10, 0.15, 0.20],
    with Joint2 located at the end of Link1.
    """
    link1_local = [(d, 0) for d in [0, 0.05, 0.10, 0.15, 0.20]]
    link2_local = [(d, 0) for d in [0, 0.05, 0.10, 0.15, 0.20]]
    
    link1_world = [rotate_point(p, theta1) for p in link1_local]
    joint2 = link1_world[-1]
    link2_world = [ (joint2[0] + rp[0], joint2[1] + rp[1])
                    for rp in [rotate_point(p, theta1+theta2) for p in link2_local] ]
    return link1_world + link2_world

###############################
# Collision Checking (Circle vs Obstacle)
###############################

def circle_rect_collision(circle_center, circle_radius, box):
    """
    Check collision between a circle and a rectangle.
    The rectangle is defined by its center, width, and height.
    """
    cx, cy = circle_center
    rx, ry = box["center"]
    w = box["width"]
    h = box["height"]
    closest_x = max(rx - w/2, min(cx, rx + w/2))
    closest_y = max(ry - h/2, min(cy, ry + h/2))
    dist = math.hypot(cx - closest_x, cy - closest_y)
    return dist <= circle_radius

def circle_circle_collision(c1, r1, c2, r2):
    """Check collision between two circles."""
    return math.hypot(c1[0]-c2[0], c1[1]-c2[1]) <= (r1 + r2)

def is_circle_in_collision(circle_center, circle_radius, obstacles):
    """
    Check if a circle (representing a robot sphere) collides with any obstacle.
    """
    for obs in obstacles:
        if obs["type"] == "box":
            if circle_rect_collision(circle_center, circle_radius, obs):
                return True
        elif obs["type"] == "sphere":
            if circle_circle_collision(circle_center, circle_radius, obs["center"], obs["radius"]):
                return True
    return False

def is_state_in_collision(theta1, theta2, obstacles):
    """
    A state (theta1, theta2) is in collision if any of the robot's circles
    (computed by robot_circle_centers) collides with an obstacle.
    """
    centers = robot_circle_centers(theta1, theta2)
    for center in centers:
        if is_circle_in_collision(center, CIRCLE_RADIUS, obstacles):
            return True
    return False

###############################
# Plotting Helpers
###############################

def plot_planning_graph(ax, edges, nodes, obstacles, title):
    """
    On the given axis, plot the planning graph:
      - Draw edges as black lines,
      - Plot all planning states as blue circles.
    """
    for parent, child in edges:
        ax.plot([parent[0], child[0]], [parent[1], child[1]], 'k-', linewidth=1)
    all_states = np.array(list(nodes))
    if len(all_states) > 0:
        ax.scatter(all_states[:,0], all_states[:,1], c='blue', marker='o')
    ax.set_title(title)
    ax.set_xlabel("Joint 1 (rad)")
    ax.set_ylabel("Joint 2 (rad)")
    ax.grid(False)

def plot_solution(ax, solution):
    """
    On the given axis, plot the solution path (nodes and edges) in red.
    Also, compute and return the solution cost as the sum of Euclidean distances
    between consecutive states.
    """
    if not solution:
        return 0.0
    sol = np.array(solution)
    # Plot solution edges in red.
    ax.plot(sol[:,0], sol[:,1], 'r-', linewidth=2, label="Solution")
    # Plot solution nodes in red.
    ax.scatter(sol[:,0], sol[:,1], c='red', marker='o', s=80)
    # Compute solution cost.
    cost = 0.0
    for i in range(len(solution)-1):
        dx = solution[i+1][0] - solution[i][0]
        dy = solution[i+1][1] - solution[i][1]
        cost += math.hypot(dx, dy)
    return cost

###############################
# Main Routine
###############################

def main():
    # File paths (adjust as needed)
    search_file1 = "/home/beno/TezaETF/code/dok_ne_skontam_sto/manip.txt"
    search_file2 = "/home/beno/TezaETF/code/dok_ne_skontam_sto/manip_dist.txt"
    scene_file = "/home/beno/TezaETF/code/bur_search_workspace/src/bur_search_motion_planning/smpl/smpl_test/planar_arm/planar_2dof_datasets/scene000"
    
    # Read command line parameter.
    if len(sys.argv) < 2:
        print("Usage: python plot_searchV2.py <param>")
        sys.exit(1)
    param = sys.argv[1]
    scene_file = scene_file + param + ".yaml"
    
    # Parse planning files (edges, nodes, and solution path).
    edges1, nodes1, sol1 = parse_search_file(search_file1)
    edges2, nodes2, sol2 = parse_search_file(search_file2)
    
    # Parse scene and extract obstacles.
    scene = parse_scene_yaml(scene_file)
    obstacles = get_obstacles(scene)
    
    # Compute configuration space collision grid.
    theta_vals = np.arange(-math.pi, math.pi + RESOLUTION, RESOLUTION)
    grid = np.zeros((len(theta_vals), len(theta_vals)), dtype=int)
    for i, t1 in enumerate(theta_vals):
        for j, t2 in enumerate(theta_vals):
            if is_state_in_collision(t1, t2, obstacles):
                grid[j, i] = 1
    
    # Create two subplots for the two planning files.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), sharex=True, sharey=True)
    extent = [-math.pi, math.pi, -math.pi, math.pi]
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(["white", "lightcoral"])
    for ax in [ax1, ax2]:
        ax.imshow(grid, origin='lower', extent=extent, cmap=cmap, alpha=0.5)
    
    # Plot planning graphs.
    plot_planning_graph(ax1, edges1, nodes1, obstacles, "Fixed motion primitives")
    plot_planning_graph(ax2, edges2, nodes2, obstacles, "Burs of free C-space")
    
    # Plot the solution path (in red) on both subplots (if available) and get solution cost.
    cost1 = plot_solution(ax1, sol1) if sol1 else 0.0
    cost2 = plot_solution(ax2, sol2) if sol2 else 0.0
    
    # Add legends that include the solution cost.
    # (If both solutions exist and differ, you could decide which one to show.)
    if sol1:
        ax1.legend(title=f"Solution cost: {cost1:.3f}")
    if sol2:
        ax2.legend(title=f"Solution cost: {cost2:.3f}")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

