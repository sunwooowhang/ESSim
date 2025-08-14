"""Main"""

import numpy as np
import network_generation
from kuramoto_simulation import run_kuramoto_until_converged_solve_ivp
import plot

# --------------------------------------------------------------------------- #
# Graph Config
# --------------------------------------------------------------------------- #

N = 100
DEGREE = 4
PROBABILITY = 0.4
TIME_STEP = 0.05
GRAPH_PARAMS_DP = 2
K_MIN = 0
K_MAX = 5
K_STEPS = 100



# --------------------------------------------------------------------------- #
# Generate network
# --------------------------------------------------------------------------- #

G_dict = network_generation.generate_ws_graph_with_info(N, DEGREE, PROBABILITY)
G = G_dict["graph"]
theta0 = np.random.uniform(0, 2 * np.pi, size=N)

# This line will print the graph stats
network_generation.print_graph_stats(G_dict, round_to=GRAPH_PARAMS_DP)


# --------------------------------------------------------------------------- #
# Sweep K
# --------------------------------------------------------------------------- #

# Forward Sweep
r_values = []
k_values = np.linspace(K_MIN, K_MAX, K_STEPS)
final_thetas = []
for K in k_values:
    r_val, _, final_theta = run_kuramoto_until_converged_solve_ivp(G, K, theta0, dt=TIME_STEP)
    r_values.append(r_val)
    print(f"K = {K:.2f}, r = {r_val:.4f}")
    final_thetas = final_theta

# Backward Sweep if possible
if final_thetas is not None:
    back_r_values = []
    for K in k_values:
        r_val, _, final_theta = run_kuramoto_until_converged_solve_ivp(G, K, final_thetas, dt=TIME_STEP)
        back_r_values.append(r_val)
        print(f"K = {K:.2f}, r = {r_val:.4f}")


# --------------------------------------------------------------------------- #
# Plot
# --------------------------------------------------------------------------- #

plot.plot_k_vs_r(k_values, r_values, save_path="plots/forward_sweep.png")
plot.plot_k_vs_r(k_values, back_r_values, save_path="plots/backward_sweep.png")
