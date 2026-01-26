import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from collections import defaultdict

# Set path to the extracted results directory
base_path = Path("../experiments/results")  # Adjust this if needed

# Output directory for plots
plot_output_dir = Path("../experiments/results/plots/time_init_exp_init")
plot_output_dir.mkdir(parents=True, exist_ok=True)

# Robot configurations and scenario labels
robots = ["planar_2DoF", "planar_7DoF"]
scenarios = {
    "scene0001": "EASY",
    "scene0002": "MEDIUM",
    "scene0003": "HARD"
}

for robot in robots:
    for scene_key, difficulty in scenarios.items():
        scene_path = base_path / robot / scene_key
        if not scene_path.exists():
            continue

        data = defaultdict(lambda: {"manip": [], "manip_dist": []})
        for file in sorted(scene_path.glob("*.csv")):
            try:
                mprim_len = int(file.stem.split("-")[1])
            except (IndexError, ValueError):
                continue

            variant = "manip_dist" if "dist" in file.stem else "manip"
            df = pd.read_csv(file)
            df = df[df["time_init"] < 60]  # Skip failed runs
            if df.empty:
                continue

            data[mprim_len][variant].append({
                "time_init": df["time_init"].mean(),
                "exp_init": df["exp_init"].mean()
            })

        # Prepare plot data
        mprim_lengths = sorted(data.keys())
        time_manip = [data[m]["manip"][0]["time_init"] if data[m]["manip"] else None for m in mprim_lengths]
        time_dist = [data[m]["manip_dist"][0]["time_init"] if data[m]["manip_dist"] else None for m in mprim_lengths]
        exp_manip = [data[m]["manip"][0]["exp_init"] if data[m]["manip"] else None for m in mprim_lengths]
        exp_dist = [data[m]["manip_dist"][0]["exp_init"] if data[m]["manip_dist"] else None for m in mprim_lengths]

        # Plot time_init
        plt.figure()
        plt.plot(mprim_lengths, time_manip, marker='o', label='Fixed primitives')
        plt.plot(mprim_lengths, time_dist, marker='s', label='Burs')
        plt.xticks(mprim_lengths)  # Integer ticks
        plt.xlabel("Motion primitive length")
        plt.ylabel("t[{}]".format("s" if "7DoF" in robot else "ms"))
        plt.title(r"$\texttt{{{}}}$ - Initial planning time".format(f"{robot}_{difficulty}"), usetex=True)
        plt.legend()
        plt.savefig(plot_output_dir / f"{robot}_{difficulty}_time_init.png")
        plt.close()

        # Plot exp_init
        plt.figure()
        plt.plot(mprim_lengths, exp_manip, marker='o', label='Fixed primitives')
        plt.plot(mprim_lengths, exp_dist, marker='s', label='Burs')
        plt.xticks(mprim_lengths)
        plt.xlabel("Motion primitive length")
        plt.ylabel("n")
        plt.title(r"$\texttt{{{}}}$ - Initial expansions".format(f"{robot}_{difficulty}"), usetex=True)
        plt.legend()
        plt.savefig(plot_output_dir / f"{robot}_{difficulty}_exp_init.png")
        plt.close()	
