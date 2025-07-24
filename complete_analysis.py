#!/usr/bin/env python3
"""
Complete Game Analysis Suite
Single file to run all simulations and generate visualizations
"""

import sys
import os
import json
import time
import random
import copy
from datetime import datetime

# Visualization imports
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle

# Set academic style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Add games directory to path
sys.path.append('games')

# Import game classes
from tic_tac_toe import TicTacToe
import nim
from Halving import HalvingGame

# Import Connect4 with strict checking
try:
    sys.path.append('games/connect4')
    from connect4 import ConnectFour
    import test as c4f
    # Verify C extension functions work
    c4f.find_best(0, 0, 2)
    c4f.win(0)
    CONNECT4_AVAILABLE = True
    print("✓ Connect4 C extension loaded successfully")
except Exception as e:
    print(f"✗ Connect4 C extension failed: {e}")
    CONNECT4_AVAILABLE = False
    ConnectFour = None
    c4f = None

def run_tic_tac_toe_simulations(num_games=200):
    """Run actual Tic-Tac-Toe simulations"""
    print("Running Tic-Tac-Toe simulations...")
    
    results = {
        'agent_vs_random': {'wins': 0, 'draws': 0, 'losses': 0, 'total_moves': 0},
        'agent_vs_agent': {'wins': 0, 'draws': 0, 'losses': 0, 'total_moves': 0},
        'random_vs_random': {'wins': 0, 'draws': 0, 'losses': 0, 'total_moves': 0}
    }
    
    # Agent vs Random
    for i in range(num_games):
        game = TicTacToe()
        moves = 0
        
        while not game.game_over:
            if game.player == 1:  # X - Agent
                row, col = game.find_best_move()
                game.make_move(row, col)
            else:  # O - Random
                moves_available = game.get_available_moves()
                if moves_available:
                    row, col = random.choice(moves_available)
                    game.make_move(row, col)
            moves += 1
        
        results['agent_vs_random']['total_moves'] += moves
        if game.winner == 1:
            results['agent_vs_random']['wins'] += 1
        elif game.winner == 2:
            results['agent_vs_random']['losses'] += 1
        else:
            results['agent_vs_random']['draws'] += 1
    
    # Agent vs Agent
    for i in range(num_games):
        game = TicTacToe()
        moves = 0
        
        while not game.game_over:
            row, col = game.find_best_move()
            game.make_move(row, col)
            moves += 1
        
        results['agent_vs_agent']['total_moves'] += moves
        if game.winner == 1:
            results['agent_vs_agent']['wins'] += 1
        elif game.winner == 2:
            results['agent_vs_agent']['losses'] += 1
        else:
            results['agent_vs_agent']['draws'] += 1
    
    # Random vs Random
    for i in range(num_games):
        game = TicTacToe()
        moves = 0
        
        while not game.game_over:
            moves_available = game.get_available_moves() 
            if moves_available:
                row, col = random.choice(moves_available)
                game.make_move(row, col)
            moves += 1
        
        results['random_vs_random']['total_moves'] += moves
        if game.winner == 1:
            results['random_vs_random']['wins'] += 1
        elif game.winner == 2:
            results['random_vs_random']['losses'] += 1
        else:
            results['random_vs_random']['draws'] += 1
    
    # Calculate statistics
    stats = {}
    for scenario in results:
        total = num_games
        win_rate = (results[scenario]['wins'] / total) * 100
        draw_rate = (results[scenario]['draws'] / total) * 100
        loss_rate = (results[scenario]['losses'] / total) * 100
        avg_moves = results[scenario]['total_moves'] / total
        
        stats[scenario] = {
            'win_rate': win_rate,
            'draw_rate': draw_rate,
            'loss_rate': loss_rate,
            'avg_game_length': avg_moves,
            'total_games': total
        }
    
    return stats

def run_connect4_simulations(num_games=100):
    """Run actual Connect4 simulations - MUST use real game methods"""
    print("Running Connect4 simulations...")
    
    if not CONNECT4_AVAILABLE:
        print("  ✗ Connect4 simulation FAILED - C extension not available")
        print("  ✗ No fallback data will be used")
        return None
    
    results = {}
    
    # 1. Agent vs Random at depth 8
    print(f"  Running Agent vs Random (depth 8): {num_games} games...")
    agent_wins = 0
    total_moves = 0
    total_time = 0
    
    for i in range(num_games):
        game = ConnectFour()
        moves = 0
        
        while True:
            if game.current_player == 'X':  # Agent
                move_start = time.time()
                col = game.best_move(8)
                move_time = time.time() - move_start
                total_time += move_time
                game.make_move(col)
            else:  # Random player
                valid_moves = game.get_valid_moves()
                if valid_moves:
                    col = random.choice(valid_moves)
                    game.make_move(col)
                else:
                    break
            
            moves += 1
            
            # Check win condition using C extension
            if c4f.win(game.bitboard['X']):
                agent_wins += 1
                break
            elif c4f.win(game.bitboard['O']):
                break
            elif not game.get_valid_moves():
                break
        
        total_moves += moves
        
        if (i + 1) % 20 == 0:
            print(f"    Completed {i + 1}/{num_games} games")
    
    results['agent_vs_random_depth8'] = {
        'win_rate': (agent_wins / num_games) * 100,
        'avg_game_length': total_moves / num_games,
        'avg_time_per_move': total_time / max(1, total_moves),
        'total_games': num_games
    }
    
    # 2. Depth comparison
    print("  Running depth comparison...")
    depths = [2, 4, 6, 8]
    depth_results = {}
    
    for depth in depths:
        print(f"    Testing depth {depth}...")
        wins = 0
        depth_time = 0
        moves_count = 0
        test_games = min(25, num_games // 4)
        
        for i in range(test_games):
            game = ConnectFour()
            
            while True:
                if game.current_player == 'X':  # Agent
                    start = time.time()
                    col = game.best_move(depth)
                    depth_time += time.time() - start
                    moves_count += 1
                    game.make_move(col)
                else:  # Random
                    valid_moves = game.get_valid_moves()
                    if valid_moves:
                        col = random.choice(valid_moves)
                        game.make_move(col)
                    else:
                        break
                
                if c4f.win(game.bitboard['X']):
                    wins += 1
                    break
                elif c4f.win(game.bitboard['O']):
                    break
                elif not game.get_valid_moves():
                    break
        
        depth_results[f'depth_{depth}'] = {
            'win_rate': (wins / test_games) * 100,
            'avg_time': depth_time / max(1, moves_count)
        }
    
    results['depth_comparison'] = depth_results
    
    # 3. Agent vs Agent
    print("  Running Agent vs Agent (depth 8 vs 6)...")
    depth8_wins = 0
    depth6_wins = 0
    agent_moves = 0
    agent_games = 25
    
    for i in range(agent_games):
        game = ConnectFour()
        moves = 0
        
        while True:
            if game.current_player == 'X':  # Depth 8
                col = game.best_move(8)
            else:  # Depth 6
                col = game.best_move(6)
            
            game.make_move(col)
            moves += 1
            
            if c4f.win(game.bitboard['X']):
                depth8_wins += 1
                break
            elif c4f.win(game.bitboard['O']):
                depth6_wins += 1
                break
            elif not game.get_valid_moves():
                break
        
        agent_moves += moves
        
        if (i + 1) % 5 == 0:
            print(f"    Completed {i + 1}/{agent_games} games")
    
    results['ai_vs_ai_depth_comparison'] = {
        'depth_8_vs_depth_6': {
            'depth_8_wins': depth8_wins,
            'depth_6_wins': depth6_wins,
            'total_games': agent_games,
            'avg_game_length': agent_moves / agent_games
        }
    }
    
    return results

def run_nim_simulations(num_games=200):
    """Run actual Nim simulations"""
    print("Running Nim simulations...")
    
    configurations = [
        [3, 4, 5], [1, 2, 3], [2, 4, 6],
        [1, 3, 5, 7], [1, 1, 1], [5, 6, 7]
    ]
    
    results = {}
    
    for config in configurations:
        config_name = str(config)
        nim_sum = nim.calculate_nim_sum(config)
        
        wins = 0
        total_moves = 0
        total_nodes = 0
        
        for i in range(num_games):
            winner, length, moves, nodes = nim.simulate_game(
                agent1_type="nim_sum",
                agent2_type="random",
                initial_piles=config.copy(),
                depth=8
            )
            
            if winner == 1:
                wins += 1
            total_moves += length
            total_nodes += nodes
        
        results[config_name] = {
            'nim_sum': nim_sum,
            'win_rate': (wins / num_games) * 100,
            'avg_game_length': total_moves / num_games,
            'avg_nodes_per_game': total_nodes / num_games,
            'total_games': num_games
        }
    
    # Overall performance
    overall_stats = nim.run_simulation_batch(
        num_games=num_games,
        agent1_type="nim_sum",
        agent2_type="random",
        initial_piles=[3, 4, 5],
        depth=8
    )
    
    return {
        'configurations': results,
        'overall': {
            'win_rate': overall_stats['agent1_win_rate'],
            'avg_game_length': overall_stats['avg_game_length'],
            'avg_nodes_per_game': overall_stats['avg_nodes_per_game'],
            'total_games': num_games
        }
    }

def run_halving_simulations(num_games=100):
    """Run actual Halving game simulations"""
    print("Running Halving game simulations...")
    
    initial_numbers = [10, 15, 20, 25, 30, 50]
    results = {}
    
    for initial_num in initial_numbers:
        wins = 0
        total_moves = 0
        
        for i in range(num_games):
            game = HalvingGame(initial_num)
            current_number = initial_num
            current_player = 1
            moves = 0
            
            while current_number > 1:
                is_maximizing = (current_player == 1)
                _, move = game.minimax(current_number, is_maximizing)
                current_number = move
                current_player = 2 if current_player == 1 else 1
                moves += 1
            
            winner = 2 if current_player == 1 else 1
            if winner == 1:
                wins += 1
            total_moves += moves
        
        results[initial_num] = {
            'win_rate': (wins / num_games) * 100,
            'avg_game_length': total_moves / num_games,
            'total_games': num_games
        }
    
    return results

def create_visualizations(data):
    """Create all academic visualizations"""
    print("Generating academic visualizations...")
    
    os.makedirs('output/images', exist_ok=True)
    
    # 1. Win Rate Comparison
    fig, ax = plt.subplots(figsize=(12, 8))
    
    games = ['Tic-Tac-Toe', 'Connect4', 'Nim', 'Halving']
    win_rates = []
    
    # Calculate win rates
    win_rates.append(data['tic_tac_toe']['agent_vs_random']['win_rate'])
    
    if data['connect4'] is not None:
        win_rates.append(data['connect4']['agent_vs_random_depth8']['win_rate'])
    else:
        win_rates.append(0)  # Failed simulation
    
    win_rates.append(data['nim']['overall']['win_rate'])
    win_rates.append(np.mean([data['halving'][n]['win_rate'] for n in [10, 15, 20, 25, 30, 50]]))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    bars = ax.bar(games, win_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
    
    # Add value labels
    for bar, rate in zip(bars, win_rates):
        height = bar.get_height()
        if rate > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{rate:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
        else:
            ax.text(bar.get_x() + bar.get_width()/2., 5,
                    'FAILED', ha='center', va='bottom', fontsize=12, fontweight='bold', color='red')
    
    ax.set_ylabel('Win Rate (%)', fontsize=14, fontweight='bold')
    ax.set_title('Algorithmic Agent Performance Across Game Types\n(Agent vs Random Player)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 110)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=50, color='red', linestyle='--', alpha=0.7, label='Random Performance')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('output/images/game_win_rates_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Performance Analysis
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Game lengths
    lengths = []
    lengths.append(data['tic_tac_toe']['agent_vs_random']['avg_game_length'])
    
    if data['connect4'] is not None:
        lengths.append(data['connect4']['agent_vs_random_depth8']['avg_game_length'])
    else:
        lengths.append(0)
    
    lengths.append(data['nim']['overall']['avg_game_length'])
    lengths.append(np.mean([data['halving'][str(n)]['avg_game_length'] for n in [10, 15, 20, 25, 30, 50]]))
    
    bars1 = ax1.bar(games, lengths, color=colors, alpha=0.8)
    ax1.set_ylabel('Average Game Length (moves)', fontweight='bold')
    ax1.set_title('Average Game Duration', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    for bar, length in zip(bars1, lengths):
        height = bar.get_height()
        if height > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{length:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Connect4 depth analysis (if available)
    if data['connect4'] is not None and 'depth_comparison' in data['connect4']:
        depths = list(data['connect4']['depth_comparison'].keys())
        depth_nums = [int(d.split('_')[1]) for d in depths]
        times = [data['connect4']['depth_comparison'][d]['avg_time'] for d in depths]
        
        ax2.plot(depth_nums, times, 'o-', linewidth=3, markersize=8, color='#e74c3c')
        ax2.set_xlabel('Search Depth', fontweight='bold')
        ax2.set_ylabel('Average Time per Move (s)', fontweight='bold')
        ax2.set_title('Connect4: Search Depth vs Computation Time', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_yscale('log')
    else:
        ax2.text(0.5, 0.5, 'Connect4 Simulation\nFAILED', ha='center', va='center', 
                transform=ax2.transAxes, fontsize=16, color='red', fontweight='bold')
        ax2.set_title('Connect4: Analysis Failed', fontweight='bold')
    
    # Nim configurations
    nim_configs = list(data['nim']['configurations'].keys())
    nim_rates = [data['nim']['configurations'][config]['win_rate'] for config in nim_configs]
    config_names = [config.replace('[', '').replace(']', '').replace(' ', '') for config in nim_configs]
    
    x_pos = np.arange(len(config_names))
    bars3 = ax3.bar(x_pos, nim_rates, color='#2ecc71', alpha=0.8)
    ax3.set_xlabel('Initial Configuration', fontweight='bold')
    ax3.set_ylabel('Win Rate (%)', fontweight='bold')
    ax3.set_title('Nim: Win Rate by Initial Configuration', fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(config_names, rotation=45)
    ax3.grid(True, alpha=0.3)
    
    for bar, rate in zip(bars3, nim_rates):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.0f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Halving patterns
    halving_nums = [10, 15, 20, 25, 30, 50]
    halving_rates = [data['halving'][str(n)]['win_rate'] for n in halving_nums]
    
    ax4.plot(halving_nums, halving_rates, 'o-', linewidth=3, markersize=8, color='#f39c12')
    ax4.set_xlabel('Initial Number', fontweight='bold')
    ax4.set_ylabel('Win Rate (%)', fontweight='bold')
    ax4.set_title('Halving Game: Win Rate by Starting Number', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(-5, 105)
    
    for x, y in zip(halving_nums, halving_rates):
        ax4.annotate(f'{y:.0f}%', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.tight_layout()
    plt.savefig('output/images/performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("  ✓ Visualizations created successfully")

def main():
    """Run complete analysis"""
    print("=" * 60)
    print("COMPLETE GAME ANALYSIS SUITE")
    print("=" * 60)
    
    all_results = {}
    
    # Run all simulations
    all_results['tic_tac_toe'] = run_tic_tac_toe_simulations(200)
    all_results['connect4'] = run_connect4_simulations(100)  # Can return None if failed
    all_results['nim'] = run_nim_simulations(200)
    all_results['halving'] = run_halving_simulations(100)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/comprehensive_simulation_results_{timestamp}.json"
    
    os.makedirs('output', exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    # Create visualizations
    create_visualizations(all_results)
    
    # Print summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    
    print(f"\nTic-Tac-Toe: {all_results['tic_tac_toe']['agent_vs_random']['win_rate']:.1f}% win rate")
    
    if all_results['connect4'] is not None:
        print(f"Connect4: {all_results['connect4']['agent_vs_random_depth8']['win_rate']:.1f}% win rate")
    else:
        print("Connect4: SIMULATION FAILED")
    
    print(f"Nim: {all_results['nim']['overall']['win_rate']:.1f}% win rate")
    
    halving_avg = np.mean([data['win_rate'] for data in all_results['halving'].values()])
    print(f"Halving: {halving_avg:.1f}% average win rate")
    
    print(f"\nResults saved to: {filename}")
    print("Visualizations saved to: output/images/")
    
    return all_results

if __name__ == "__main__":
    results = main()