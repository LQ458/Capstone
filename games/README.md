# Game Simulation Project

This project contains AI implementations and simulation analysis of multiple classic games, using different search algorithms to study game strategies and performance.

## Project Structure

```
games/
├── README.md                    # This file
├── tic_tac_toe.py              # Tic-Tac-Toe game implementation
├── connect4.py                  # Connect4 game implementation
├── Halving.py                   # Halving game implementation
├── test.c                       # Connect4 C extension
├── test.pyx                     # Connect4 Cython interface
├── setup.py                     # Compilation script
├── test.cpython-313-darwin.so   # Compiled extension
├── connect4/                    # Connect4 game folder
│   ├── connect4_simulation.py   # Connect4 simulation code
│   └── connect4_visualization.py # Connect4 visualization code
└── halving/                     # Halving game folder
    ├── halving_simulation.py    # Halving simulation code
    └── halving_visualization.py # Halving visualization code
```

## Game Implementations

### Tic-Tac-Toe
- **File**: `tic_tac_toe.py`
- **Algorithm**: Minimax with alpha-beta pruning
- **Features**: Complete game tree exploration, optimal play

### Connect4
- **File**: `connect4.py`
- **Algorithm**: Minimax with bitboard optimization
- **Features**: C extension for performance, depth-limited search

### Halving Game
- **File**: `Halving.py`
- **Algorithm**: Minimax with mathematical strategy
- **Features**: Exponential state space, optimal strategy analysis

## Usage

Each game can be run independently:

```bash
# Tic-Tac-Toe
python tic_tac_toe.py

# Connect4
python connect4.py

# Halving Game
python Halving.py
```

## Simulation and Analysis

The project includes comprehensive simulation and analysis tools:

- **Performance Testing**: Agent vs random player simulations
- **Strategy Analysis**: Opening move distributions and optimal play patterns
- **Visualization**: Charts and graphs showing game statistics
- **Comparative Analysis**: Cross-game performance comparisons

## Requirements

- Python 3.7+
- NumPy
- Matplotlib
- Cython (for Connect4 C extension)

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Compile C extensions: `python setup.py build_ext --inplace`
4. Run simulations: `python generate_all_visualizations.py` 