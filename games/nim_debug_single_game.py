#!/usr/bin/env python3
"""
Debug a single game to understand the issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nim import NimGame, calculate_nim_sum, optimal_nim_move, find_best_move, simulate_game

def debug_single_game():
    """Debug a single game step by step"""
    print("=== DEBUGGING SINGLE GAME ===\n")
    
    config = [1, 2, 3]  # Losing position
    print(f"Initial config: {config}")
    print(f"Initial nim-sum: {calculate_nim_sum(config)}")
    print()
    
    # Run a single game with verbose output
    winner, length, moves, nodes = simulate_game(
        agent1_type="nim_sum",
        agent2_type="random", 
        initial_piles=config,
        depth=8,
        verbose=True
    )
    
    print(f"\nFinal result: Player {winner} won in {length} moves")
    print(f"Move sequence: {moves}")

if __name__ == "__main__":
    debug_single_game() 