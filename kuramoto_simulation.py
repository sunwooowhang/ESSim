"""Kuramoto simulation"""

import numpy as np
from scipy.integrate import solve_ivp
import networkx as nx

def _get_theta_dot(graph, K, current_theta):
    """Compute the time derivative of the phase of each node in the Kuramoto model."""
    A = nx.to_numpy_array(graph)
    theta_diff = current_theta[None, :] - current_theta[:, None]

    # Modification 1 : Natural frequency is proportional to the degree of the node (s.f. 1 for now)
    natural_frequency = np.array([deg for _, deg in graph.degree()])

    #Modification 2 : Normalization by dividing the node degree (In case the graph is not so connected)
    degrees = np.array([deg for _, deg in graph.degree()])
    degrees = np.where(degrees == 0, 1, degrees)  # prevent divide-by-zero

    coupling_term = np.sum(A * np.sin(theta_diff), axis=1)
    theta_dot = natural_frequency + (K / degrees) * coupling_term

    return theta_dot

def _compute_order_parameter(theta):
    """Compute the Kuramoto order parameter r from the phase vector theta"""
    N = len(theta)
    return np.abs(np.sum(np.exp(1j * theta)) / N)

def _integrate_theta_solve_ivp(graph, K, theta0, t_max=100, dt=0.05):
    """Integrate the Kuramoto model using solve_ivp and the shared _get_theta_dot function."""
    def kuramoto_rhs(t, theta):
        return _get_theta_dot(graph, K, theta)

    t_span = (0, t_max)
    t_eval = np.arange(0, t_max, dt)

    sol = solve_ivp(kuramoto_rhs, t_span, theta0, t_eval=t_eval, method="DOP853", rtol=1e-8, atol=1e-10)

    return sol.t, sol.y.T # Notice we don't really need the t values, none of our graphs are time-dependent

def run_kuramoto_until_converged_solve_ivp(graph, K, theta0, dt=0.05, t_max=500, r_tol=1e-4, r_window=100):
    """
    Simulate the Kuramoto model using solve_ivp until the order parameter r stabilizes.
    Returns the last r value, the history of r values, and the theta history.
    If the r values do not converge, it returns None for final theta.
    """
    t, theta_hist = _integrate_theta_solve_ivp(graph, K, theta0, t_max=t_max, dt=dt) # Saving t just in case
    r_values = np.abs(np.mean(np.exp(1j * theta_hist), axis=1))

    for i in range(r_window, len(r_values)):
        recent_r = r_values[i - r_window:i]
        if np.max(np.abs(recent_r - recent_r[-1])) < r_tol:
            print("r converged to a stable value")
            final_theta = theta_hist[i].flatten()
            return r_values[i], r_values[:i+1], final_theta

    print("r did not converge to a stable value")
    return r_values[-1], r_values, None
