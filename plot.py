"""Plotting functions"""

import matplotlib.pyplot as plt
import os

# Define plotting functions for various graphs

def plot_k_vs_r(k_values, r_values, save_path="plots/k_vs_r.png"):
    plt.figure(figsize=(8, 6))
    plt.plot(k_values, r_values, marker='o', linestyle='none')
    plt.xlabel("Coupling strength K")
    plt.ylabel("Order parameter r")
    plt.title("K vs r")
    plt.grid(True)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()

def plot_C_vs_kcf(C_values, kcf_values, save_path="plots/C_vs_kcf.png"):
    plt.figure(figsize=(8, 6))
    plt.plot(C_values, kcf_values, marker='o', linestyle='none')
    plt.xlabel("Clustering coefficient C")
    plt.ylabel("Critical forward K")
    plt.title("C vs K_cf")
    plt.grid(True)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()

def plot_C_vs_kcb(C_values, kcb_values, save_path="plots/C_vs_kcb.png"):
    plt.figure(figsize=(8, 6))
    plt.plot(C_values, kcb_values, marker='o', linestyle='none')
    plt.xlabel("Clustering coefficient C")
    plt.ylabel("Critical backward K")
    plt.title("C vs K_cb")
    plt.grid(True)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()

def plot_C_vs_deltaK(C_values, deltaK_values, save_path="plots/C_vs_deltaK.png"):
    plt.figure(figsize=(8, 6))
    plt.plot(C_values, deltaK_values, marker='o', linestyle='none')
    plt.xlabel("Clustering coefficient C")
    plt.ylabel("Delta K (K_cf - K_cb)")
    plt.title("C vs ΔK")
    plt.grid(True)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()

