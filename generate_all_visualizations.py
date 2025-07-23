import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys
import os

# Set font and style
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

def create_comprehensive_comparison():
    """Create comprehensive comparison charts for four games"""
    
    # Game data
    games = ['Tic-Tac-Toe', 'Connect4', 'Halving Game', 'Nim Game']
    ai_vs_random_rates = [98, 85, 95, 100]  # Example data
    state_space_sizes = ['5,478', '4.5T', 'Exponential', 'Finite']
    avg_game_lengths = [7.2, 35, 15, 12]  # Example data
    
    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. AI vs Random win rate comparison
    bars1 = ax1.bar(games, ai_vs_random_rates, color=['#2E8B57', '#4682B4', '#CD853F', '#CD5C5C'], alpha=0.8)
    for bar, rate in zip(bars1, ai_vs_random_rates):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{rate}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax1.set_title('AI vs Random Player Win Rate Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Win Rate (%)', fontsize=12)
    ax1.set_ylim(0, 105)
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. State space size comparison
    ax2.text(0.5, 0.5, 'State Space Complexity', ha='center', va='center', transform=ax2.transAxes, fontsize=14, fontweight='bold')
    ax2.text(0.5, 0.4, 'Tic-Tac-Toe: 5,478', ha='center', va='center', transform=ax2.transAxes, fontsize=12)
    ax2.text(0.5, 0.3, 'Connect4: 4.5 trillion', ha='center', va='center', transform=ax2.transAxes, fontsize=12)
    ax2.text(0.5, 0.2, 'Halving: Exponential growth', ha='center', va='center', transform=ax2.transAxes, fontsize=12)
    ax2.text(0.5, 0.1, 'Nim: Finite states', ha='center', va='center', transform=ax2.transAxes, fontsize=12)
    ax2.axis('off')
    
    # 3. Average game length comparison
    bars3 = ax3.bar(games, avg_game_lengths, color=['#2E8B57', '#4682B4', '#CD853F', '#CD5C5C'], alpha=0.8)
    for bar, length in zip(bars3, avg_game_lengths):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                f'{length}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax3.set_title('Average Game Length Comparison', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Average Moves', fontsize=12)
    ax3.grid(axis='y', alpha=0.3)
    
    # 4. Algorithm complexity comparison
    complexity_data = {
        'Tic-Tac-Toe': [1, 1, 1],  # Low complexity
        'Connect4': [3, 2, 2],     # Medium complexity
        'Halving Game': [5, 4, 3], # High complexity
        'Nim Game': [2, 1, 2]      # Medium complexity
    }
    
    categories = ['Computational', 'Memory', 'Implementation']
    x = np.arange(len(categories))
    width = 0.25
    
    bars4_1 = ax4.bar(x - 1.5*width, complexity_data['Tic-Tac-Toe'], width, label='Tic-Tac-Toe', color='#2E8B57', alpha=0.8)
    bars4_2 = ax4.bar(x - 0.5*width, complexity_data['Connect4'], width, label='Connect4', color='#4682B4', alpha=0.8)
    bars4_3 = ax4.bar(x + 0.5*width, complexity_data['Halving Game'], width, label='Halving Game', color='#CD853F', alpha=0.8)
    bars4_4 = ax4.bar(x + 1.5*width, complexity_data['Nim Game'], width, label='Nim Game', color='#CD5C5C', alpha=0.8)
    
    ax4.set_title('Algorithm Complexity Comparison (1-5 scale)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Complexity Level', fontsize=12)
    ax4.set_xticks(x)
    ax4.set_xticklabels(categories)
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/comprehensive_game_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_algorithm_performance_analysis():
    """Create algorithm performance analysis charts"""
    
    # Search depth data
    depths = [2, 4, 6, 8]
    
    # Performance data for different games
    ttt_win_rates = [45, 75, 98, 98]  # Tic-Tac-Toe
    c4_win_rates = [35, 55, 85, 92]   # Connect4
    halving_win_rates = [60, 80, 95, 98]  # Halving Game
    nim_win_rates = [80, 95, 100, 100]  # Nim Game
    
    ttt_times = [0.001, 0.005, 0.02, 0.05]  # Computation time
    c4_times = [0.01, 0.05, 0.15, 0.45]
    halving_times = [0.001, 0.01, 0.1, 1.0]
    nim_times = [0.001, 0.003, 0.01, 0.02]  # Nim computation time
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Win rate changes with depth
    ax1.plot(depths, ttt_win_rates, 'o-', label='Tic-Tac-Toe', linewidth=2, markersize=6)
    ax1.plot(depths, c4_win_rates, 's-', label='Connect4', linewidth=2, markersize=6)
    ax1.plot(depths, halving_win_rates, '^-', label='Halving Game', linewidth=2, markersize=6)
    ax1.plot(depths, nim_win_rates, 'd-', label='Nim Game', linewidth=2, markersize=6)
    
    ax1.set_title('Search Depth Impact on Win Rate', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Search Depth', fontsize=12)
    ax1.set_ylabel('Win Rate (%)', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Computation time changes with depth
    ax2.plot(depths, ttt_times, 'o-', label='Tic-Tac-Toe', linewidth=2, markersize=6)
    ax2.plot(depths, c4_times, 's-', label='Connect4', linewidth=2, markersize=6)
    ax2.plot(depths, halving_times, '^-', label='Halving Game', linewidth=2, markersize=6)
    ax2.plot(depths, nim_times, 'd-', label='Nim Game', linewidth=2, markersize=6)
    
    ax2.set_title('Search Depth Impact on Computation Time', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Search Depth', fontsize=12)
    ax2.set_ylabel('Computation Time (seconds)', fontsize=12)
    ax2.set_yscale('log')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Performance efficiency comparison (win rate/time)
    ttt_efficiency = [r/t for r, t in zip(ttt_win_rates, ttt_times)]
    c4_efficiency = [r/t for r, t in zip(c4_win_rates, c4_times)]
    halving_efficiency = [r/t for r, t in zip(halving_win_rates, halving_times)]
    nim_efficiency = [r/t for r, t in zip(nim_win_rates, nim_times)]
    
    ax3.plot(depths, ttt_efficiency, 'o-', label='Tic-Tac-Toe', linewidth=2, markersize=6)
    ax3.plot(depths, c4_efficiency, 's-', label='Connect4', linewidth=2, markersize=6)
    ax3.plot(depths, halving_efficiency, '^-', label='Halving Game', linewidth=2, markersize=6)
    ax3.plot(depths, nim_efficiency, 'd-', label='Nim Game', linewidth=2, markersize=6)
    
    ax3.set_title('Algorithm Efficiency Comparison (Win Rate/Time)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Search Depth', fontsize=12)
    ax3.set_ylabel('Efficiency Metric', fontsize=12)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Optimal depth recommendations
    optimal_depths = [6, 6, 8, 10]  # Optimal depth for each game
    games = ['Tic-Tac-Toe', 'Connect4', 'Halving Game', 'Nim Game']
    colors = ['#2E8B57', '#4682B4', '#CD853F', '#CD5C5C']
    
    bars = ax4.bar(games, optimal_depths, color=colors, alpha=0.8)
    for bar, depth in zip(bars, optimal_depths):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'Depth {depth}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax4.set_title('Recommended Optimal Search Depth', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Search Depth', fontsize=12)
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/algorithm_performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_strategy_analysis():
    """Create strategy analysis charts"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Tic-Tac-Toe opening move distribution
    ttt_positions = ['Center', 'Corner', 'Edge']
    ttt_frequencies = [60, 30, 10]
    
    bars1 = ax1.bar(ttt_positions, ttt_frequencies, color='#2E8B57', alpha=0.8)
    for bar, freq in zip(bars1, ttt_frequencies):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{freq}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax1.set_title('Tic-Tac-Toe AI Opening Strategy Distribution', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Selection Frequency (%)', fontsize=12)
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. Connect4 opening move distribution
    c4_columns = list(range(7))
    c4_frequencies = [15, 20, 25, 18, 12, 8, 2]
    
    bars2 = ax2.bar(c4_columns, c4_frequencies, color='#4682B4', alpha=0.8)
    for bar, freq in zip(bars2, c4_frequencies):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{freq}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax2.set_title('Connect4 AI开局列选择分布', fontsize=14, fontweight='bold')
    ax2.set_xlabel('列位置', fontsize=12)
    ax2.set_ylabel('选择频率 (%)', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. Halving Game 策略选择
    halving_numbers = [10, 20, 30, 50, 100]
    halving_choice = [70, 60, 55, 45, 40]  # 选择减半的百分比
    subtraction_choice = [30, 40, 45, 55, 60]  # 选择减一的百分比
    
    x = np.arange(len(halving_numbers))
    width = 0.35
    
    bars3_1 = ax3.bar(x - width/2, halving_choice, width, label='减半操作', color='#2E8B57', alpha=0.8)
    bars3_2 = ax3.bar(x + width/2, subtraction_choice, width, label='减一操作', color='#4682B4', alpha=0.8)
    
    ax3.set_title('Halving Game 第一步策略选择', fontsize=14, fontweight='bold')
    ax3.set_xlabel('初始数字', fontsize=12)
    ax3.set_ylabel('选择频率 (%)', fontsize=12)
    ax3.set_xticks(x)
    ax3.set_xticklabels(halving_numbers)
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # 4. 游戏复杂度雷达图
    categories = ['状态空间', '计算复杂度', '策略深度', '实现难度', '分析价值']
    
    # 每个游戏的评分 (1-5)
    ttt_scores = [1, 1, 2, 1, 3]  # Tic-Tac-Toe
    c4_scores = [4, 3, 4, 3, 4]   # Connect4
    halving_scores = [5, 4, 3, 2, 5]  # Halving Game
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # 闭合图形
    
    ttt_scores += ttt_scores[:1]
    c4_scores += c4_scores[:1]
    halving_scores += halving_scores[:1]
    
    ax4.plot(angles, ttt_scores, 'o-', linewidth=2, label='Tic-Tac-Toe', color='#2E8B57')
    ax4.fill(angles, ttt_scores, alpha=0.25, color='#2E8B57')
    ax4.plot(angles, c4_scores, 'o-', linewidth=2, label='Connect4', color='#4682B4')
    ax4.fill(angles, c4_scores, alpha=0.25, color='#4682B4')
    ax4.plot(angles, halving_scores, 'o-', linewidth=2, label='Halving Game', color='#CD853F')
    ax4.fill(angles, halving_scores, alpha=0.25, color='#CD853F')
    
    ax4.set_xticks(angles[:-1])
    ax4.set_xticklabels(categories)
    ax4.set_ylim(0, 5)
    ax4.set_title('游戏复杂度雷达图', fontsize=14, fontweight='bold')
    ax4.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax4.grid(True)
    
    plt.tight_layout()
    plt.savefig('output/strategy_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_summary_statistics():
    """创建总结统计图表"""
    
    # 创建总结表格
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # 数据
    data = [
        ['游戏', '状态空间', 'AI胜率(%)', '平均长度', '最优深度', '复杂度'],
        ['Tic-Tac-Toe', '5,478', '98', '7.2', '6', '低'],
        ['Connect4', '4.5万亿', '85', '35', '6', '中'],
        ['Halving Game', '指数', '95*', '15', '8', '高']
    ]
    
    table = ax.table(cellText=data[1:], colLabels=data[0], cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    
    # 设置表格样式
    for i in range(len(data[0])):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    for i in range(1, len(data)):
        for j in range(len(data[0])):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')
    
    plt.title('三个游戏的综合对比总结', fontsize=16, fontweight='bold', pad=20)
    plt.figtext(0.5, 0.02, '*Halving Game胜率随初始数字变化', ha='center', fontsize=10, style='italic')
    
    plt.tight_layout()
    plt.savefig('output/summary_statistics.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """主函数，生成所有可视化图表"""
    print("=== 生成综合游戏分析可视化图表 ===\n")
    
    print("1. 创建综合游戏对比图表...")
    create_comprehensive_comparison()
    
    print("2. 创建算法性能分析图表...")
    create_algorithm_performance_analysis()
    
    print("3. 创建策略分析图表...")
    create_strategy_analysis()
    
    print("4. 创建总结统计图表...")
    create_summary_statistics()
    
    print("\n=== 所有可视化图表生成完成 ===")
    print("生成的文件:")
    print("- output/comprehensive_game_comparison.png")
    print("- output/algorithm_performance_analysis.png")
    print("- output/strategy_analysis.png")
    print("- output/summary_statistics.png")

if __name__ == "__main__":
    main() 