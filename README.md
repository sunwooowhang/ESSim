# ES Simulation

A Python simulation project for studying synchronization phenomena using the Kuramoto model on complex networks.

## Description

This project implements a simulation of the Kuramoto model to study synchronization in complex networks. It includes:

- Network generation with different topologies
- Kuramoto model simulation with parameter sweeps
- Visualization of synchronization behavior
- Analysis of critical coupling strength

## Files

- `main.py` - Main execution script
- `kuramoto_simulation.py` - Kuramoto model implementation
- `network_generation.py` - Network topology generation
- `plot.py` - Visualization and plotting functions
- `requirements.txt` - Python dependencies
- `plots/` - Generated plot outputs

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main simulation:
```bash
python main.py
```

This will generate plots showing the synchronization behavior and save them in the `plots/` directory.

## Dependencies

- numpy
- matplotlib
- networkx
- scipy

See `requirements.txt` for specific versions. 
