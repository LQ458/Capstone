#!/usr/bin/env python3
"""
Academic Visualization Generator for Game AI Analysis
Generates publication-quality figures for LaTeX report
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle
import os

# Set academic style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Load real simulation data
with open('output/comprehensive_simulation_results_20250723_222623.json', 'r') as f:
    data = json.load(f)

# Create output directory
os.makedirs('output/images', exist_ok=True)

def create_win_rate_comparison():
    """Create comprehensive win rate comparison across all games"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    games = ['Tic-Tac-Toe', 'Connect4', 'Nim', 'Halving']
    win_rates = [
        data['tic_tac_toe']['agent_vs_random']['win_rate'],
        data['connect4']['agent_vs_random_depth8']['win_rate'],
        data['nim']['overall']['win_rate'],
        np.mean([data['halving'][str(n)]['win_rate'] for n in [10, 15, 20, 25, 30, 50]])
    ]
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    bars = ax.bar(games, win_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
    
    # Add value labels on bars
    for bar, rate in zip(bars, win_rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Win Rate (%)', fontsize=14, fontweight='bold')
    ax.set_title('Algorithmic Agent Performance Across Game Types\n(Agent vs Random Player)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 110)
    ax.grid(True, alpha=0.3)
    
    # Add horizontal line at 50% for reference
    ax.axhline(y=50, color='red', linestyle='--', alpha=0.7, label='Random Performance')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('output/images/game_win_rates_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_performance_metrics():
    """Create performance metrics visualization"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Game Length Analysis
    games = ['Tic-Tac-Toe', 'Connect4', 'Nim', 'Halving']
    avg_lengths = [
        data['tic_tac_toe']['agent_vs_random']['avg_game_length'],
        data['connect4']['agent_vs_random_depth8']['avg_game_length'],
        data['nim']['overall']['avg_game_length'],
        np.mean([data['halving'][str(n)]['avg_game_length'] for n in [10, 15, 20, 25, 30, 50]])
    ]
    
    bars1 = ax1.bar(games, avg_lengths, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'], alpha=0.8)
    ax1.set_ylabel('Average Game Length (moves)', fontweight='bold')
    ax1.set_title('Average Game Duration', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    for bar, length in zip(bars1, avg_lengths):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{length:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Connect4 Depth Performance
    depths = list(data['connect4']['depth_comparison'].keys())
    depth_nums = [int(d.split('_')[1]) for d in depths]
    times = [data['connect4']['depth_comparison'][d]['avg_time'] for d in depths]
    
    ax2.plot(depth_nums, times, 'o-', linewidth=3, markersize=8, color='#e74c3c')
    ax2.set_xlabel('Search Depth', fontweight='bold')
    ax2.set_ylabel('Average Time per Move (s)', fontweight='bold')
    ax2.set_title('Connect4: Search Depth vs Computation Time', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')
    
    # 3. Nim Configuration Analysis
    nim_configs = list(data['nim']['configurations'].keys())
    nim_win_rates = [data['nim']['configurations'][config]['win_rate'] for config in nim_configs]
    nim_lengths = [data['nim']['configurations'][config]['avg_game_length'] for config in nim_configs]
    
    # Simplify config names for display
    config_names = [config.replace('[', '').replace(']', '').replace(' ', '') for config in nim_configs]
    
    x_pos = np.arange(len(config_names))
    bars3 = ax3.bar(x_pos, nim_win_rates, color='#2ecc71', alpha=0.8)
    ax3.set_xlabel('Initial Configuration', fontweight='bold')
    ax3.set_ylabel('Win Rate (%)', fontweight='bold')
    ax3.set_title('Nim: Win Rate by Initial Configuration', fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(config_names, rotation=45)
    ax3.grid(True, alpha=0.3)
    
    for bar, rate in zip(bars3, nim_win_rates):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.0f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 4. Halving Game Pattern Analysis
    halving_nums = [10, 15, 20, 25, 30, 50]
    halving_rates = [data['halving'][str(n)]['win_rate'] for n in halving_nums]
    
    ax4.plot(halving_nums, halving_rates, 'o-', linewidth=3, markersize=8, color='#f39c12')
    ax4.set_xlabel('Initial Number', fontweight='bold')
    ax4.set_ylabel('Win Rate (%)', fontweight='bold')
    ax4.set_title('Halving Game: Win Rate by Starting Number', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(-5, 105)
    
    # Add annotations for pattern
    for x, y in zip(halving_nums, halving_rates):
        ax4.annotate(f'{y:.0f}%', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.tight_layout()
    plt.savefig('output/images/performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_algorithm_effectiveness():
    """Create algorithm effectiveness comparison"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Win Rate vs Random Baseline
    games = ['Tic-Tac-Toe', 'Connect4', 'Nim', 'Halving*']
    win_rates = [97.5, 100.0, 100.0, 50.0]  # Halving average marked with asterisk
    random_baseline = [50, 50, 50, 50]
    
    x = np.arange(len(games))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, win_rates, width, label='Algorithmic Agent', color='#2ecc71', alpha=0.8)
    bars2 = ax1.bar(x + width/2, random_baseline, width, label='Random Baseline', color='#95a5a6', alpha=0.8)
    
    ax1.set_xlabel('Game Type', fontweight='bold')
    ax1.set_ylabel('Win Rate (%)', fontweight='bold')
    ax1.set_title('Agent Performance vs Random Baseline', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(games)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 110)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.0f}%', ha='center', va='bottom', fontsize=10)
    
    # 2. Computational Efficiency (nodes per game)
    games_nodes = ['Tic-Tac-Toe', 'Nim']
    nodes_per_game = [100, data['nim']['overall']['avg_nodes_per_game']]  # TTT estimated from game tree
    
    bars3 = ax2.bar(games_nodes, nodes_per_game, color=['#3498db', '#2ecc71'], alpha=0.8)
    ax2.set_xlabel('Game Type', fontweight='bold')
    ax2.set_ylabel('Average Nodes Evaluated per Game', fontweight='bold')
    ax2.set_title('Computational Efficiency', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    for bar, nodes in zip(bars3, nodes_per_game):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{nodes:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/images/algorithm_effectiveness.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_comprehensive_summary():
    """Create comprehensive summary table visualization"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare data for table
    table_data = [
        ['Game', 'State Space', 'AI Win Rate (%)', 'Avg Game Length', 'Optimal Depth', 'Key Strategy'],
        ['Tic-Tac-Toe', '5,478 positions', '97.5', '5.7 moves', '6', 'Complete tree search'],
        ['Connect4', '4.5 trillion positions', '100.0', '11.0 moves', '8', 'Alpha-beta + heuristics'],
        ['Nim', 'Variable (finite)', '100.0*', '6.5 moves', 'N/A', 'Nim-sum mathematical'],
        ['Halving', 'Exponential growth', '50.0**', '7.2 moves', '8', 'Mathematical analysis']
    ]
    
    # Create table
    table = ax.table(cellText=table_data[1:], colLabels=table_data[0], 
                    cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    
    # Header styling
    for i in range(len(table_data[0])):
        table[(0, i)].set_facecolor('#34495e')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(table_data)):
        for j in range(len(table_data[0])):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#ecf0f1')
            else:
                table[(i, j)].set_facecolor('white')
    
    # Win rate column highlighting
    for i in range(1, len(table_data)):
        win_rate = float(table_data[i][2].replace('*', ''))
        if win_rate >= 95:
            table[(i, 2)].set_facecolor('#d5f4e6')  # Light green
        elif win_rate >= 80:
            table[(i, 2)].set_facecolor('#fff2cc')  # Light yellow
        else:
            table[(i, 2)].set_facecolor('#ffeaa7')  # Light orange
    
    ax.set_title('Comprehensive Game AI Analysis Summary\n', fontsize=16, fontweight='bold', pad=20)
    
    # Add footnotes
    footnote_text = "*Perfect play with nim-sum heuristic\n**Varies significantly with initial number (0-100%)"
    ax.text(0.5, -0.1, footnote_text, transform=ax.transAxes, ha='center', 
            fontsize=10, style='italic', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
    
    plt.savefig('output/images/comprehensive_summary.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_search_depth_analysis():
    """Create search depth performance analysis"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Connect4 depth analysis
    depths = [2, 4, 6, 8]
    times = [0.0, 0.0, 0.001, 0.007]
    win_rates = [100, 100, 100, 100]
    
    # Left plot: Time complexity
    ax1.semilogy(depths, [max(t, 0.0001) for t in times], 'o-', linewidth=3, markersize=8, color='#e74c3c')
    ax1.set_xlabel('Search Depth', fontweight='bold')
    ax1.set_ylabel('Computation Time per Move (s)', fontweight='bold')
    ax1.set_title('Connect4: Search Depth Impact on Performance', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0.0001, 0.1)
    
    # Add annotations
    for x, y in zip(depths, times):
        ax1.annotate(f'{y:.3f}s' if y > 0 else '<0.001s', (x, max(y, 0.0001)), 
                    textcoords="offset points", xytext=(0,10), ha='center')
    
    # Right plot: Theoretical complexity comparison
    games = ['Tic-Tac-Toe', 'Connect4', 'Nim', 'Halving']
    complexity_scores = [1, 4, 2, 3]  # Relative complexity (1=lowest, 4=highest)
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    
    bars = ax2.bar(games, complexity_scores, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
    ax2.set_ylabel('Computational Complexity (Relative)', fontweight='bold')
    ax2.set_title('Game Complexity Comparison', fontweight='bold')
    ax2.set_ylim(0, 5)
    ax2.grid(True, alpha=0.3)
    
    # Add complexity labels
    complexity_labels = ['Low', 'Very High', 'Medium', 'High']
    for bar, label in zip(bars, complexity_labels):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                label, ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/images/search_depth_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Generate all academic visualizations"""
    print("Generating academic visualizations...")
    
    print("  → Creating win rate comparison...")
    create_win_rate_comparison()
    
    print("  → Creating performance metrics...")
    create_performance_metrics()
    
    print("  → Creating algorithm effectiveness...")
    create_algorithm_effectiveness()
    
    print("  → Creating search depth analysis...")
    create_search_depth_analysis()
    
    print("  → Creating comprehensive summary...")
    create_comprehensive_summary()
    
    print("All visualizations generated successfully!")
    print("Files saved to output/images/:")
    print("  - game_win_rates_comparison.png")
    print("  - performance_analysis.png") 
    print("  - algorithm_effectiveness.png")
    print("  - search_depth_analysis.png")
    print("  - comprehensive_summary.png")

if __name__ == "__main__":
    main()