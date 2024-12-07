# Cache Simulator with GUI

This project is a Python-based simulator for a simple memory caching system. It features both instruction and data caches and includes a graphical user interface (GUI) to enhance user interaction.

## Features
- **Direct-Mapped Cache Simulation**: Simulates a one-level, read-only, direct-mapped cache with configurable parameters.
- **Separate Instruction and Data Caches**: Tracks hits, misses, and performance metrics separately for instruction and data caches. The user provides two separate access sequences: one for instructions and one for data.
- **User-Configurable Parameters**:
  - Total cache size
  - Line size
  - Cache and memory access times
- **Graphical User Interface (GUI)**:
  - Load input files directly via the GUI.
  - Step-by-step simulation controls.
  - Displays detailed outputs, including hit/miss results and AMAT calculations.

## How It Works
The simulator processes memory access sequences for both instructions and data. It calculates the following metrics for each cache:
- Cache hits and misses
- Hit and miss ratios
- Average Memory Access Time (AMAT)

Users can load memory access sequences through the GUI or provide them in the console.

### Input Sequences
The user is required to provide two separate sequences of memory addresses:
- **Instruction Access Sequence**: A sequence of memory addresses for instruction accesses.
- **Data Access Sequence**: A sequence of memory addresses for data accesses.

Both sequences will be processed separately in the instruction and data caches. The user will load the instruction and data sequences via the GUI or as input files.

## Requirements
- Python 3.8+
- Libraries:
  - `tkinter` (for GUI)
  - `os` (for file handling)
