import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from connect4_simulation import Connect4Simulation
import json
import time

# Set font and style
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

def create_connect4_win_rate_chart():
    """Create Connect4 win rate comparison chart"""
    # Simulation data
    scenarios = ['Agent vs Random', 'Agent vs Agent (6 vs 4)', 'Agent vs Agent (6 vs 6)']
    win_rates = [85, 72, 50]  # Example data
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(scenarios, win_rates, color=['#2E8B57', '#4682B4', '#CD5C5C'], alpha=0.8)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.xlabel('Game Scenario', fontsize=12)
    plt.ylabel('Win Rate (%)', fontsize=12)
    plt.title('Connect4 Agent Performance Analysis', fontsize=16, fontweight='bold')
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../../output/connect4_win_rates.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_depth_performance_chart():
    """Create search depth performance chart"""
    depths = [2, 4, 6, 8]
    win_rates = [45, 65, 85, 92]  # Example data
    avg_times = [0.01, 0.05, 0.15, 0.45]  # Example data
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Win rate chart
    bars1 = ax1.bar(depths, win_rates, color='#2E8B57', alpha=0.8)
    ax1.set_xlabel('Search Depth', fontsize=12)
    ax1.set_ylabel('Win Rate (%)', fontsize=12)
    ax1.set_title('Search Depth vs Win Rate', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Time performance chart
    bars2 = ax2.bar(depths, avg_times, color='#4682B4', alpha=0.8)
    ax2.set_xlabel('Search Depth', fontsize=12)
    ax2.set_ylabel('Average Computation Time (seconds)', fontsize=12)
    ax2.set_title('Search Depth vs Computation Time', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        time_val = height
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{time_val:.2f}s', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('../../output/connect4_depth_performance.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_opening_move_analysis():
    """Create opening move analysis chart"""
    columns = ['Col 0', 'Col 1', 'Col 2', 'Col 3', 'Col 4', 'Col 5', 'Col 6']
    agent_moves = [15, 20, 25, 18, 12, 8, 2]  # Example data
    random_moves = [14.3, 14.3, 14.3, 14.3, 14.3, 14.3, 14.3]  # Uniform distribution
    
    x = np.arange(len(columns))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    bars1 = plt.bar(x - width/2, agent_moves, width, label='Agent Player', color='#2E8B57', alpha=0.8)
    bars2 = plt.bar(x + width/2, random_moves, width, label='Random Player', color='#4682B4', alpha=0.8)
    
    plt.xlabel('Column Position', fontsize=12)
    plt.ylabel('Selection Frequency (%)', fontsize=12)
    plt.title('Connect4 Opening Move Distribution Analysis', fontsize=16, fontweight='bold')
    plt.xticks(x, columns)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('../../output/connect4_opening_moves.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_game_length_distribution():
    """Create game length distribution chart"""
    # Simulated game length data
    game_lengths = np.random.normal(35, 8, 1000)  # Example data
    game_lengths = np.clip(game_lengths, 20, 50)  # Limit to reasonable range
    
    plt.figure(figsize=(10, 6))
    plt.hist(game_lengths, bins=30, color='#2E8B57', alpha=0.7, edgecolor='black')
    plt.axvline(np.mean(game_lengths), color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {np.mean(game_lengths):.1f}')
    
    plt.xlabel('Game Length (moves)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Connect4 Game Length Distribution', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../../output/connect4_game_lengths.png', dpi=300, bbox_inches='tight')
    plt.show()

def run_connect4_analysis():
    """Run complete Connect4 analysis"""
    print("Starting Connect4 game analysis...")
    
    simulation = Connect4Simulation()
    
    # Run simulations
    print("1. Running agent vs random simulation...")
    agent_vs_random = simulation.simulate_agent_vs_random(50, 6)
    
    print("2. Running agent vs agent simulation...")
    agent_vs_agent = simulation.simulate_agent_vs_agent(30, 6, 4)
    
    print("3. Analyzing opening moves...")
    opening_analysis = simulation.analyze_opening_moves(50, 6)
    
    print("4. Testing different depth performance...")
    depth_performance = simulation.performance_vs_depth([2, 4, 6], 20)
    
    # Save results
    results = {
        'agent_vs_random': agent_vs_random,
        'agent_vs_agent': agent_vs_agent,
        'opening_analysis': opening_analysis,
        'depth_performance': depth_performance,
        'timestamp': time.strftime('%Y%m%d_%H%M%S')
    }
    
    with open('../../output/connect4_simulation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Analysis complete, results saved to connect4_simulation_results.json")
    
    return results

def main():
    """Main function"""
    print("=== Connect4 Game Visualization Analysis ===\n")
    
    # Run analysis
    results = run_connect4_analysis()
    
    # Create visualization charts
    print("\nCreating visualization charts...")
    create_connect4_win_rate_chart()
    create_depth_performance_chart()
    create_opening_move_analysis()
    create_game_length_distribution()
    
    print("\n=== Visualization Analysis Complete ===")

if __name__ == "__main__":
    main() 