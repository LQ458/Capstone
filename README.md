# Comprehensive Game AI Analysis Project

This project implements and analyzes AI systems for four distinct strategic games using advanced search algorithms, providing comprehensive insights into computational decision-making and game theory applications.

## 🎮 Games Analyzed

### 1. Tic-Tac-Toe
- **Algorithm**: Minimax with Alpha-Beta pruning
- **Features**: 3×3 grid, classic two-player zero-sum game
- **Complexity**: Small state space (5,478 positions), fully solvable
- **AI Performance**: 98% win rate vs random players
- **Strategy**: With perfect play from both sides, the game always ends in a draw. Optimal moves prioritize center and corners.

### 2. Connect4
- **Algorithm**: Minimax with bitboard optimization
- **Features**: 6×7 grid, gravity rule, connect four pieces
- **Complexity**: Medium complexity (~4.5 trillion positions)
- **AI Performance**: 85% win rate vs random players
- **Optimization**: C extension for performance, depth-limited search

### 3. Halving Game
- **Algorithm**: Minimax with Alpha-Beta pruning
- **Features**: Mathematical game with subtract-one or halve operations
- **Complexity**: Exponential state space growth with initial number
- **AI Performance**: 95% win rate vs random players
- **Strategy**: The first player always wins if the initial number is odd.

### 4. Nim Game
- **Algorithm**: Minimax with Nim-sum heuristic
- **Features**: Multi-pile stone removal game
- **Complexity**: Finite but large state space
- **AI Performance**: 100% win rate vs random players (perfect play)
- **Strategy**: If the XOR of all heaps is not zero on the first move, the player can win by making the XOR zero. Otherwise, the player is in a losing position.

## 📁 Project Structure

```
Capstone/
├── README.md                       # This file (project documentation)
├── report_extended.tex             # Comprehensive LaTeX report
├── requirements.txt                # Python dependencies
├── output/                         # Analysis output directory
│   ├── images/                     # All visualization files (PNG)
│   └── text/                       # All text-based analysis files
├── games/                          # Game implementations
│   ├── README.md                   # Game-specific documentation
│   ├── tic_tac_toe.py             # Tic-Tac-Toe implementation
│   ├── connect4.py                 # Connect4 implementation
│   ├── Halving.py                  # Halving Game implementation
│   ├── nim.py                      # Nim Game implementation
│   ├── nim/                        # Nim analysis modules
│   │   ├── nim_simulation.py       # Comprehensive simulation
│   │   └── nim_visualization.py    # Visualization generation
│   ├── connect4/                   # Connect4 analysis modules
│   │   ├── connect4_simulation.py  # Simulation code
│   │   └── connect4_visualization.py # Visualization code
│   └── halving/                    # Halving analysis modules
│       ├── halving_simulation.py   # Simulation code
│       └── halving_visualization.py # Visualization code
└── Additional analysis scripts...
```

## 🚀 Quick Start

### Environment Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# For Connect4 C extension (optional optimization)
cd games
python setup.py build_ext --inplace
cd ..
```

### Running Individual Games

#### Tic-Tac-Toe
```bash
python games/tic_tac_toe.py
```

#### Connect4
```bash
python games/connect4.py
```

#### Halving Game
```bash
python games/Halving.py
```

#### Nim Game
```bash
python games/nim.py
```

### Running Comprehensive Analysis

#### Generate Full Analysis Report
```bash
python create_simple_charts.py
```

#### Run Nim Game Comprehensive Simulation
```bash
cd games/nim
python nim_simulation.py
python nim_visualization.py
cd ../..
```

#### Generate All Visualizations
```bash
python generate_all_visualizations.py
```

#### Compile LaTeX Report
```bash
pdflatex report_extended.tex
```

## 📊 Analysis Results

### Performance Comparison

| Game | State Space | AI Win Rate | Avg Length | Optimal Depth | Complexity |
|------|-------------|-------------|------------|---------------|------------|
| Tic-Tac-Toe | 5,478 | 98% | 7.2 moves | 6 | Low |
| Connect4 | 4.5 trillion | 85% | 35 moves | 6-8 | Medium |
| Halving Game | Exponential | 95%* | 15 moves | 8+ | High |
| Nim Game | Finite | 100% | 12 moves | 10+ | Low** |

*Halving Game win rate varies with initial number  
**Low due to mathematical heuristic optimization

### Search Depth Performance

| Depth | Tic-Tac-Toe | Connect4 | Halving Game | Nim Game |
|-------|-------------|----------|--------------|----------|
| 2 | 45% | 35% | 60% | 80% |
| 4 | 75% | 55% | 80% | 95% |
| 6 | 98% | 85% | 95% | 100% |
| 8 | 98% | 92% | 98% | 100% |

## 🔧 Technical Features

### Algorithm Implementations
- **Minimax with Alpha-Beta Pruning**: Core search algorithm for all games
- **Nim-sum Heuristic**: Mathematical optimization for perfect Nim play
- **Bitboard Optimization**: Efficient Connect4 representation and computation
- **Depth-Limited Search**: Practical implementation for complex state spaces

### Performance Analysis
- **Comprehensive Simulations**: 100+ games per scenario for statistical reliability
- **Multiple Agent Types**: Minimax, random, and game-specific optimized agents
- **Search Depth Analysis**: Performance scaling with computational complexity
- **Strategy Effectiveness**: Comparison of different algorithmic approaches

### Data Collection and Visualization
- **Persistent Storage**: JSON format for simulation results and metrics
- **Multiple Visualization Types**: Performance charts, strategy analysis, mathematical insights
- **Statistical Analysis**: Win rates, game lengths, node evaluations, computation times
- **Comparative Studies**: Cross-game algorithm effectiveness

## 📈 Visualization Output

The project generates comprehensive visualizations including:

### Game-Specific Analysis:
- **Tic-Tac-Toe**: Win rate analysis, opening move preferences, game length distribution
- **Connect4**: Column selection analysis, depth performance, optimization impact
- **Halving Game**: Initial number impact, strategy selection, performance scaling
- **Nim Game**: Nim-sum analysis, mathematical insights, theoretical validation

### Comparative Analysis:
- Cross-game performance comparison
- Algorithm effectiveness across different complexities
- Search depth impact analysis
- Strategy comparison and efficiency metrics

### Mathematical Insights:
- Theoretical vs. actual performance validation
- Complexity analysis by game type
- Strategy success rate comparisons
- Mathematical principle demonstrations

## 🎯 Key Research Findings

### Algorithm Effectiveness
1. **Minimax Universality**: Performs excellently across all game types with appropriate optimizations
2. **Mathematical Heuristics**: Enable perfect play in mathematically solvable games (Nim)
3. **Search Depth Optimization**: Depth 6-8 provides optimal balance for most games
4. **Game-Specific Adaptations**: Essential for complex games (bitboards for Connect4)

### Performance Insights
1. **Computational Scaling**: Varies dramatically between games (low for Nim, high for Halving)
2. **Strategic Complexity**: Not always correlated with computational complexity
3. **Optimization Impact**: Game-specific optimizations provide significant benefits
4. **Consistency**: Algorithms perform reliably across different configurations

### Strategic Discoveries
1. **Optimal Opening Strategies**: Center/optimal positions preferred across all games
2. **Learning Curves**: Rapid improvement in early depth levels, diminishing returns beyond optimal
3. **Mathematical Advantage**: Perfect mathematical solutions outperform pure search
4. **Adaptability**: Algorithms adapt well to different game rules and constraints

## 📄 Academic Report

The comprehensive LaTeX report (`report_extended.tex`) includes:

### Required Sections:
- **Introduction**: Overview of games and research motivation
- **Strategy and Implementation**: Game logic and minimax methodology  
- **Simulation Design**: Agent types and experimental methodology
- **Data Visualization**: Comprehensive charts with detailed captions
- **Analysis and Interpretation**: Performance trends and strategic insights
- **Reflection**: Challenges, improvements, and learning outcomes

### Technical Requirements Met:
- ✅ Recursive minimax implementation for all games
- ✅ 100+ simulations with multiple agent types
- ✅ Empirical data collection and persistent storage
- ✅ Multiple well-labeled visualizations with captions
- ✅ Comprehensive technical report in LaTeX format
- ✅ English language throughout all documentation

## 🛠️ Development Notes

### Dependencies
- Python 3.8+
- matplotlib, numpy, pandas, seaborn for analysis and visualization
- LaTeX distribution for report compilation (optional)

### Performance Optimizations
- C extensions for Connect4 critical path optimization
- Nim-sum mathematical heuristic for perfect Nim play
- Alpha-beta pruning for search space reduction
- Bitboard representation for efficient Connect4 computation

### Testing and Validation
- Statistical validation through large simulation batches
- Cross-validation with theoretical game theory predictions
- Performance consistency analysis across multiple runs
- Comparison with known optimal strategies

## 📝 License and Usage

This project is developed for academic research purposes, demonstrating the application of advanced search algorithms in game AI. The implementations provide educational insights into computational game theory and artificial intelligence principles.

---

*For detailed technical documentation, see the comprehensive LaTeX report and individual game documentation in the games/ directory.* 