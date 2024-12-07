# Cache Simulator with GUI

This project is a Python-based simulator for a simple memory caching system. It features both instruction and data caches and includes a graphical user interface (GUI) to enhance user interaction.

## Features
- **Direct-Mapped Cache Simulation**: Simulates a one-level, read-only, direct-mapped cache with configurable parameters.
- **Independent Instruction and Data Caches**: Separately tracks hits, misses, and performance metrics for instruction and data caches.
- **User-Configurable Parameters**:
  - Total cache size
  - Line size
  - Cache and memory access times
- **Graphical User Interface (GUI)**:
  - Load input files directly via the GUI.
  - Step-by-step simulation controls.
  - Displays detailed outputs, including hit/miss results and AMAT calculations.

## How It Works
The simulator processes memory access sequences and calculates the following metrics:
- Cache hits and misses
- Hit and miss ratios
- Average Memory Access Time (AMAT)

Users can load memory access sequences through the GUI or provide them in the console.

## Requirements
- Python 3.8+
- Libraries:
  - `tkinter` (for GUI)
  - `os` (for file handling)

