#!/usr/bin/env python3
"""
Nim Game Mathematical Analysis Test
This script verifies the mathematical correctness of Nim game implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nim import NimGame, calculate_nim_sum, optimal_nim_move, simulate_game

def test_nim_sum_calculations():
    """Test Nim-sum calculations for different configurations"""
    print("=== NIM-SUM MATHEMATICAL ANALYSIS ===\n")
    
    test_configs = [
        ([1, 2, 3], "Losing position"),
        ([3, 4, 5], "Winning position"), 
        ([2, 4, 6], "Losing position"),
        ([1, 3, 5, 7], "Losing position"),
        ([1, 1, 1], "Winning position"),
        ([2, 2, 2], "Losing position"),
        ([1, 2, 4, 8], "Winning position")
    ]
    
    print("Configuration Analysis:")
    print("-" * 50)
    
    for config, expected in test_configs:
        nim_sum = calculate_nim_sum(config)
        is_winning = nim_sum != 0
        status = "WINNING" if is_winning else "LOSING"
        
        print(f"Config {config}: Nim-sum = {nim_sum} → {status} position")
        print(f"  Expected: {expected}")
        print(f"  First player should {'win' if is_winning else 'lose'}")
        print()
    
    return test_configs

def test_optimal_moves():
    """Test optimal move calculation"""
    print("=== OPTIMAL MOVE ANALYSIS ===\n")
    
    winning_configs = [
        [3, 4, 5],  # Nim-sum = 2
        [1, 1, 1],  # Nim-sum = 1  
        [1, 2, 4, 8]  # Nim-sum = 15
    ]
    
    for config in winning_configs:
        nim_sum = calculate_nim_sum(config)
        optimal = optimal_nim_move(config)
        
        print(f"Config {config} (Nim-sum = {nim_sum}):")
        if optimal:
            pile_idx, stones = optimal
            print(f"  Optimal move: Take {stones} stones from pile {pile_idx}")
            
            # Verify the move
            new_config = config.copy()
            new_config[pile_idx] -= stones
            new_nim_sum = calculate_nim_sum(new_config)
            print(f"  New config: {new_config} (Nim-sum = {new_nim_sum})")
            print(f"  Move is {'correct' if new_nim_sum == 0 else 'incorrect'}")
        else:
            print("  No optimal move found (should not happen for winning position)")
        print()

def test_simulation_results():
    """Test actual simulation results vs mathematical expectations"""
    print("=== SIMULATION VS MATHEMATICAL EXPECTATIONS ===\n")
    
    test_cases = [
        ([3, 4, 5], "nim_sum", "random", 100),  # Should be ~100% win rate
        ([1, 2, 3], "nim_sum", "random", 100),  # Should be ~0% win rate
        ([2, 4, 6], "nim_sum", "random", 100),  # Should be ~0% win rate
    ]
    
    for config, agent1, agent2, num_games in test_cases:
        nim_sum = calculate_nim_sum(config)
        expected_win_rate = 100 if nim_sum != 0 else 0
        
        print(f"Testing {agent1} vs {agent2} with config {config}:")
        print(f"  Nim-sum = {nim_sum}, Expected win rate = {expected_win_rate}%")
        
        # Run simulation
        winner, length, moves, nodes = simulate_game(
            agent1_type=agent1,
            agent2_type=agent2, 
            initial_piles=config,
            depth=8
        )
        
        actual_win_rate = 100 if winner == 1 else 0
        print(f"  Actual result: Player {winner} won")
        print(f"  Actual win rate: {actual_win_rate}%")
        print(f"  {'✓ PASS' if actual_win_rate == expected_win_rate else '✗ FAIL'}")
        print()

def test_perfect_play_analysis():
    """Analyze perfect play scenarios"""
    print("=== PERFECT PLAY ANALYSIS ===\n")
    
    # Test nim_sum vs nim_sum (both perfect players)
    print("Nim-sum vs Nim-sum (both perfect players):")
    config = [3, 4, 5]
    nim_sum = calculate_nim_sum(config)
    
    print(f"Config {config}: Nim-sum = {nim_sum}")
    if nim_sum != 0:
        print("First player should win with perfect play")
        print("Second player cannot win against perfect play")
    else:
        print("Second player should win with perfect play")
        print("First player cannot win against perfect play")
    
    # Run a few games to verify
    print("\nRunning 5 perfect vs perfect games:")
    for i in range(5):
        winner, length, moves, nodes = simulate_game(
            agent1_type="nim_sum",
            agent2_type="nim_sum",
            initial_piles=config,
            depth=8
        )
        print(f"  Game {i+1}: Player {winner} won in {length} moves")
    
    print()

if __name__ == "__main__":
    test_nim_sum_calculations()
    test_optimal_moves() 
    test_simulation_results()
    test_perfect_play_analysis()
    
    print("=== ANALYSIS COMPLETE ===")
    print("\nKey Findings:")
    print("1. Nim-sum = 0 → Current player is in losing position")
    print("2. Nim-sum ≠ 0 → Current player can force a win")
    print("3. Perfect play should result in deterministic outcomes")
    print("4. Win rates should be 0% or 100%, not 50%") 