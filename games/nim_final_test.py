#!/usr/bin/env python3
"""
Final test to verify the fix for Nim game losing positions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nim import NimGame, calculate_nim_sum, optimal_nim_move, find_best_move, simulate_game

def test_fixed_losing_position():
    """Test if the fix works for losing positions"""
    print("=== TESTING FIXED LOSING POSITION ===\n")
    
    # Test losing position [1, 2, 3]
    config = [1, 2, 3]
    nim_sum = calculate_nim_sum(config)
    
    print(f"Config: {config}")
    print(f"Nim-sum: {nim_sum}")
    print(f"Position type: {'LOSING' if nim_sum == 0 else 'WINNING'}")
    print()
    
    # Test find_best_move with nim_sum strategy
    game = NimGame(config)
    best_move, nodes = find_best_move(game, depth=8, use_nim_sum=True)
    print(f"find_best_move result: {best_move}, nodes={nodes}")
    
    if best_move:
        pile_idx, stones = best_move
        new_config = config.copy()
        new_config[pile_idx] -= stones
        new_nim_sum = calculate_nim_sum(new_config)
        print(f"After move {best_move}:")
        print(f"  New config: {new_config}")
        print(f"  New nim-sum: {new_nim_sum}")
        print(f"  Position type: {'LOSING' if new_nim_sum == 0 else 'WINNING'}")
    print()

def test_multiple_games():
    """Test multiple games to see win rates"""
    print("=== MULTIPLE GAMES TEST ===\n")
    
    losing_configs = [
        [1, 2, 3],
        [2, 4, 6],
        [1, 3, 5, 7]
    ]
    
    for config in losing_configs:
        nim_sum = calculate_nim_sum(config)
        print(f"Testing config {config} (Nim-sum = {nim_sum}):")
        
        # Run 10 games
        wins = 0
        for i in range(10):
            winner, length, moves, nodes = simulate_game(
                agent1_type="nim_sum",
                agent2_type="random",
                initial_piles=config,
                depth=8
            )
            if winner == 1:
                wins += 1
        
        win_rate = (wins / 10) * 100
        expected_rate = 0 if nim_sum == 0 else 100
        print(f"  Win rate: {win_rate:.0f}% (expected: {expected_rate}%)")
        print(f"  {'✓ PASS' if win_rate == expected_rate else '✗ FAIL'}")
        print()

def test_perfect_vs_perfect():
    """Test perfect vs perfect play"""
    print("=== PERFECT VS PERFECT TEST ===\n")
    
    config = [1, 2, 3]  # Losing position
    nim_sum = calculate_nim_sum(config)
    
    print(f"Config {config} (Nim-sum = {nim_sum}):")
    print("Running 10 perfect vs perfect games:")
    
    for i in range(10):
        winner, length, moves, nodes = simulate_game(
            agent1_type="nim_sum",
            agent2_type="nim_sum",
            initial_piles=config,
            depth=8
        )
        print(f"  Game {i+1}: Player {winner} won in {length} moves")
    
    print()
    print("Expected: Player 2 should win all games (since Player 1 starts in losing position)")

if __name__ == "__main__":
    test_fixed_losing_position()
    test_multiple_games()
    test_perfect_vs_perfect()
    
    print("=== SUMMARY ===")
    print("The issue was that when optimal_nim_move() returns None (losing position),")
    print("the code was falling back to minimax search, which could find a 'best' move")
    print("even though all moves lead to loss.")
    print()
    print("The fix ensures that when we're in a losing position, we make a random move")
    print("since all moves are equally bad.") 