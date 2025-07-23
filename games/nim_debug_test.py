#!/usr/bin/env python3
"""
Debug test for Nim game to understand why losing positions still win
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nim import NimGame, calculate_nim_sum, optimal_nim_move, find_best_move, minimax

def debug_losing_position():
    """Debug a specific losing position"""
    print("=== DEBUGGING LOSING POSITION ===\n")
    
    # Test losing position [1, 2, 3]
    config = [1, 2, 3]
    nim_sum = calculate_nim_sum(config)
    
    print(f"Config: {config}")
    print(f"Nim-sum: {nim_sum}")
    print(f"Position type: {'LOSING' if nim_sum == 0 else 'WINNING'}")
    print()
    
    # Test optimal_nim_move
    optimal = optimal_nim_move(config)
    print(f"optimal_nim_move result: {optimal}")
    print()
    
    # Test find_best_move with nim_sum strategy
    game = NimGame(config)
    best_move_nim, nodes_nim = find_best_move(game, depth=8, use_nim_sum=True)
    print(f"find_best_move (nim_sum=True): {best_move_nim}, nodes={nodes_nim}")
    print()
    
    # Test find_best_move without nim_sum strategy (minimax only)
    best_move_minimax, nodes_minimax = find_best_move(game, depth=8, use_nim_sum=False)
    print(f"find_best_move (nim_sum=False): {best_move_minimax}, nodes={nodes_minimax}")
    print()
    
    # Test what happens if we make the minimax move
    if best_move_minimax:
        pile_idx, stones = best_move_minimax
        new_config = config.copy()
        new_config[pile_idx] -= stones
        new_nim_sum = calculate_nim_sum(new_config)
        print(f"After minimax move {best_move_minimax}:")
        print(f"  New config: {new_config}")
        print(f"  New nim-sum: {new_nim_sum}")
        print(f"  Position type: {'LOSING' if new_nim_sum == 0 else 'WINNING'}")
    print()

def test_minimax_evaluation():
    """Test minimax evaluation of losing positions"""
    print("=== MINIMAX EVALUATION TEST ===\n")
    
    losing_configs = [
        [1, 2, 3],
        [2, 4, 6], 
        [1, 3, 5, 7]
    ]
    
    for config in losing_configs:
        nim_sum = calculate_nim_sum(config)
        print(f"Config {config} (Nim-sum = {nim_sum}):")
        
        game = NimGame(config)
        
        # Test minimax evaluation at depth 0
        eval_depth_0 = minimax(game, depth=0, is_maximizing=True)
        print(f"  Minimax eval (depth=0): {eval_depth_0}")
        
        # Test minimax evaluation at depth 2
        eval_depth_2 = minimax(game, depth=2, is_maximizing=True)
        print(f"  Minimax eval (depth=2): {eval_depth_2}")
        
        # Test minimax evaluation at depth 4
        eval_depth_4 = minimax(game, depth=4, is_maximizing=True)
        print(f"  Minimax eval (depth=4): {eval_depth_4}")
        
        print()

def test_move_generation():
    """Test move generation for losing positions"""
    print("=== MOVE GENERATION TEST ===\n")
    
    config = [1, 2, 3]
    game = NimGame(config)
    
    print(f"Config: {config}")
    print(f"Available moves: {game.generate_moves()}")
    print()
    
    # Test each possible move
    for move in game.generate_moves():
        pile_idx, stones = move
        new_config = config.copy()
        new_config[pile_idx] -= stones
        new_nim_sum = calculate_nim_sum(new_config)
        
        print(f"Move {move}: {config} → {new_config}")
        print(f"  Nim-sum: {new_nim_sum}")
        print(f"  Position type: {'LOSING' if new_nim_sum == 0 else 'WINNING'}")
        print()

def test_heuristic_evaluation():
    """Test the heuristic evaluation function"""
    print("=== HEURISTIC EVALUATION TEST ===\n")
    
    test_configs = [
        ([1, 2, 3], "Losing position"),
        ([3, 4, 5], "Winning position"),
        ([2, 2, 2], "Winning position"),  # Note: This is actually winning!
        ([1, 1, 1], "Winning position")
    ]
    
    for config, expected in test_configs:
        nim_sum = calculate_nim_sum(config)
        heuristic_value = 1 if nim_sum != 0 else -1
        
        print(f"Config {config}:")
        print(f"  Nim-sum: {nim_sum}")
        print(f"  Heuristic value: {heuristic_value}")
        print(f"  Expected: {expected}")
        print(f"  {'✓' if (nim_sum != 0) == (expected == 'Winning position') else '✗'}")
        print()

if __name__ == "__main__":
    debug_losing_position()
    test_minimax_evaluation()
    test_move_generation()
    test_heuristic_evaluation()
    
    print("=== KEY INSIGHT ===")
    print("The issue is that when nim_sum = 0 (losing position):")
    print("1. optimal_nim_move() returns None")
    print("2. find_best_move() falls back to minimax search")
    print("3. minimax finds a 'best' move even though all moves lead to loss")
    print("4. This creates the illusion that the player can win from a losing position")
    print()
    print("SOLUTION: When in a losing position, the AI should:")
    print("1. Either make a random move (since all moves are equally bad)")
    print("2. Or explicitly handle the None return from optimal_nim_move()") 