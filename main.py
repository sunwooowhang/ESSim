"""Main"""

import numpy as np
import networkx as nx
import network_generation
from kuramoto_simulation import run_kuramoto_adaptive_measure_r_mean
import plot

# --------------------------------------------------------------------------- #
# Graph Config
# --------------------------------------------------------------------------- #
# In Report, N = 1000, DEGREE = 8, TIME_STEP = 0.05 (some was changed for testing)
N = 1000
DEGREE = 8
PROBABILITY = 0.05
TIME_STEP = 0.1
T_MEASURE = 1000
T_CHUNK = 50
BLOCK_LEN = 10
M_BLOCKS = 5
GRAPH_PARAMS_DP = 2
K_MIN = 0
K_MAX = 5
K_STEPS = 50

theta0 = np.random.uniform(0, 2 * np.pi, size=N)
theta_seed = theta0.copy() # Use for starting each K with the previous K's theta_last


# --------------------------------------------------------------------------- #
# Sweep K function
# --------------------------------------------------------------------------- #
def sweep_K(G, theta_prev):
    k_values = np.linspace(K_MIN, K_MAX, K_STEPS)

    # ---------- Forward sweep ----------
    r_fwd, regimes_fwd, flags_fwd = [], [], []

    for i, K in enumerate(k_values):
        res = run_kuramoto_adaptive_measure_r_mean(
            G, K, theta_prev,                 # continuation forward; for cold-start: seed_for_forward()
            dt=TIME_STEP,
            T_chunk=T_CHUNK,
            block_length=BLOCK_LEN,
            M=M_BLOCKS,
            T_measure=T_MEASURE,
            # optionally pass eps, sigma_max, slope_tol, etc.
        )
        theta_prev = res["theta_last"]       # carry state forward (remove this if cold-start)
        r_fwd.append(res["r_mean"])
        regimes_fwd.append(res["regime"])
        flags_fwd.append(res["flags"])

        print(f"FWD  K={K:.4f} | r̄={res['r_mean']:.4f} (±{res['r_std']:.4f}) | {res['regime']}"
            + (f" | flags={res['flags']}" if res['flags'] else ""))

    # After forward, theta_seed is the final state at K_MAX (good for starting backward)

    # ---------- Backward (desync) sweep ----------
    r_down, regimes_down, flags_down = [], [], []

    for i, K in enumerate(reversed(k_values)):   # K: K_MAX -> K_MIN
        res = run_kuramoto_adaptive_measure_r_mean(
            G, K, theta_prev,                   # continuation down
            dt=TIME_STEP,
            T_chunk=T_CHUNK,
            block_length=BLOCK_LEN,
            M=M_BLOCKS,
            T_measure=T_MEASURE,
        )
        theta_prev = res["theta_last"]          # continue downhill
        r_down.append(res["r_mean"])
        regimes_down.append(res["regime"])
        flags_down.append(res["flags"])

        print(f"DOWN K={K:.4f} | r̄={res['r_mean']:.4f} (±{res['r_std']:.4f}) | {res['regime']}"
            + (f" | flags={res['flags']}" if res['flags'] else ""))

    # Align backward data with ascending K for plotting against k_values:
    r_down_aligned = r_down[::-1]   # now indexes match k_values ascending

    return k_values, r_fwd, r_down_aligned



# --------------------------------------------------------------------------- #
# Generate graph, sweep and Plot
# --------------------------------------------------------------------------- #

# Plot for different p values
p_values = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
def plot_for_p(p_values):
    """Plot for different p values"""
    for p in p_values:
        graph = nx.watts_strogatz_graph(N, DEGREE, p)
        network_generation.get_graph_stats(graph, round_to=GRAPH_PARAMS_DP)
        k_list, r_fwd_list, r_down_aligned_list = sweep_K(graph, theta_seed)

        plot.plot_k_vs_r_hysteresis(
            k_list,
            r_fwd_list,
            r_down_aligned_list,
            save_path=f"plots/hysteresis_p={p}.png"
    )

def plot_for_ba():
    """Plot for BA graph"""
    graph = nx.barabasi_albert_graph(N, DEGREE)
    network_generation.get_graph_stats(graph, round_to=GRAPH_PARAMS_DP)
    k_list, r_fwd_list, r_down_aligned_list = sweep_K(graph, theta_seed)

    plot.plot_k_vs_r_hysteresis(
        k_list,
        r_fwd_list,
        r_down_aligned_list,
        save_path=f"plots/hysteresis_BA_N={N}_m={DEGREE}.png"
    )

