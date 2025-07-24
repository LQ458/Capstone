# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Game AI Analysis Project that implements and analyzes AI systems for four strategic games (Tic-Tac-Toe, Connect4, Halving Game, and Nim) using advanced search algorithms. The project focuses on computational decision-making and game theory applications with extensive performance analysis and visualization.

## Core Architecture

### Game Implementation Pattern
Each game follows a consistent minimax architecture:
- **Core Game Logic**: Individual game files (`tic_tac_toe.py`, `connect4.py`, `Halving.py`, `nim.py`)
- **Minimax Algorithm**: Alpha-beta pruning implementation across all games
- **Game-Specific Optimizations**: 
  - Connect4: Bitboard optimization with C extension
  - Nim: Nim-sum mathematical heuristic for perfect play
  - Halving: Mathematical strategy analysis
  - Tic-Tac-Toe: Complete game tree exploration

### Analysis Framework
- **Separated Analysis**: All simulation/visualization modules are in dedicated `analysis/` directory, completely separated from core game logic
- **Unified Output**: All analysis results stored in `output/` directory (images + JSON data)
- **Comprehensive Reporting**: LaTeX academic report with all findings

### Performance Optimization Strategy
- **C Extensions**: Connect4 uses Cython/C optimization (`test.pyx`, `test.c`, `setup.py`)
- **Mathematical Heuristics**: Nim uses perfect mathematical solutions
- **Search Depth Management**: Configurable depth limits for practical performance

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Build Connect4 C extension for performance
cd games
python setup.py build_ext --inplace
cd ..
```

### Running Individual Games
```bash
python games/tic_tac_toe.py      # Tic-Tac-Toe
python games/connect4.py         # Connect4
python games/Halving.py          # Halving Game
python games/nim.py              # Nim Game
```

### Analysis and Visualization
```bash
# Run complete analysis suite (recommended)
python run_analysis.py

# Or run components individually:
python run_comprehensive_simulations.py      # Generate real simulation data
python generate_academic_visualizations.py  # Create publication-quality figures

# Run specific game analysis (optional)
python analysis/nim/nim_simulation.py
python analysis/connect4/connect4_simulation.py
python analysis/halving/halving_simulation.py
python analysis/tic_tac_toe/tic_tac_toe_comprehensive_simulation.py
```

### Report Generation
```bash
# Compile LaTeX report (requires LaTeX installation)
./compile_extended_report.sh
# or manually:
pdflatex report_extended.tex
```

## File Organization Principles

### Critical Paths
- **Output Directory**: `output/` - ALL generated analysis files (images + JSON) go here
- **Games Directory**: `games/` - ONLY core game implementations (game logic files)
- **Analysis Directory**: `analysis/` - Comprehensive simulation modules for each game
- **LaTeX Report**: `report_extended.tex` - Single comprehensive academic report

### Essential Files
- **`run_analysis.py`** - Single script to run complete analysis suite
- **`run_comprehensive_simulations.py`** - Generate real simulation data across all games
- **`generate_academic_visualizations.py`** - Create publication-quality figures
- **Core Games**: `games/tic_tac_toe.py`, `games/connect4/connect4.py`, `games/Halving.py`, `games/nim.py`

### Module Structure
- **Clean Separation**: Core game logic in `games/` directory contains ONLY essential game files
  - Connect4 includes C extension files (`test.pyx`, `test.c`, `setup.py`) for performance optimization
- **Streamlined Analysis**: Essential simulation modules in `analysis/` subdirectories
- **Unified Output**: All results saved to centralized `output/` directory (images + data)
- **Academic Quality**: All visualizations designed for publication standards

### Dependencies
- **Core**: matplotlib, numpy, pandas, seaborn (from requirements.txt)
- **Optional**: Cython (for Connect4 optimization), LaTeX (for report compilation)

## Key Technical Insights

### Algorithm Implementation
- All games use minimax with alpha-beta pruning as base algorithm
- Game-specific optimizations are crucial for performance (especially Connect4 bitboards and Nim mathematical solutions)
- Search depth of 6-8 provides optimal balance across most games

### Performance Characteristics
- **Tic-Tac-Toe**: Small state space (5,478 positions), 98% win rate
- **Connect4**: Large state space (~4.5 trillion), 85% win rate, benefits heavily from C optimization
- **Halving Game**: Exponential complexity, 95% win rate, performance varies with initial number
- **Nim**: Finite but large space, 100% win rate with mathematical heuristic

### Data Flow
1. Games generate simulation data during analysis runs
2. All output (images, JSON) saved to centralized `output/` directory
3. LaTeX report references output files for comprehensive academic documentation
4. Visualization scripts can be run independently or as part of comprehensive analysis

## Testing and Validation
- No formal unit test framework present
- Validation through statistical simulation (100+ games per scenario)
- Cross-validation with theoretical game theory predictions
- Performance consistency analysis across multiple runs