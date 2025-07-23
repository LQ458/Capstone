import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from connect4_simulation import Connect4Simulation
import json
import time

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

def create_connect4_win_rate_chart():
    """创建Connect4胜率对比图表"""
    # 模拟数据
    categories = ['Bot vs Random', 'Bot vs Bot (6 vs 4)', 'Bot vs Bot (6 vs 6)']
    win_rates = [85, 72, 50]  # 示例数据
    colors = ['#2E8B57', '#4682B4', '#CD853F']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, win_rates, color=colors, alpha=0.8)
    
    # 添加数值标签
    for bar, rate in zip(bars, win_rates):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{rate}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.title('Connect4 Bot Performance Against Different Opponents', fontsize=16, fontweight='bold')
    plt.ylabel('Win Rate (%)', fontsize=12)
    plt.ylim(0, 105)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../../output/connect4_win_rates.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_depth_performance_chart():
    """创建搜索深度性能图表"""
    depths = [2, 4, 6, 8]
    win_rates = [45, 65, 85, 92]  # 示例数据
    avg_times = [0.01, 0.05, 0.15, 0.45]  # 示例数据
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 胜率图表
    bars1 = ax1.bar(depths, win_rates, color='#2E8B57', alpha=0.8)
    for bar, rate in zip(bars1, win_rates):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{rate}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax1.set_title('搜索深度对胜率的影响', fontsize=14, fontweight='bold')
    ax1.set_xlabel('搜索深度', fontsize=12)
    ax1.set_ylabel('胜率 (%)', fontsize=12)
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)
    
    # 时间性能图表
    bars2 = ax2.bar(depths, avg_times, color='#4682B4', alpha=0.8)
    for bar, time_val in zip(bars2, avg_times):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{time_val:.2f}s', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax2.set_title('搜索深度对计算时间的影响', fontsize=14, fontweight='bold')
    ax2.set_xlabel('搜索深度', fontsize=12)
    ax2.set_ylabel('平均计算时间 (秒)', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../../output/connect4_depth_performance.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_opening_move_analysis():
    """创建开局移动分析图表"""
    columns = list(range(7))
    bot_moves = [15, 20, 25, 18, 12, 8, 2]  # 示例数据
    random_moves = [14.3, 14.3, 14.3, 14.3, 14.3, 14.3, 14.3]  # 均匀分布
    
    x = np.arange(len(columns))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    bars1 = plt.bar(x - width/2, bot_moves, width, label='Bot Player', color='#2E8B57', alpha=0.8)
    bars2 = plt.bar(x + width/2, random_moves, width, label='Random Player', color='#4682B4', alpha=0.8)
    
    plt.xlabel('Column Position', fontsize=12)
plt.ylabel('Selection Frequency (%)', fontsize=12)
plt.title('Connect4 Opening Move Distribution Analysis', fontsize=16, fontweight='bold')
    plt.xticks(x, columns)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('../../output/connect4_opening_moves.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_game_length_distribution():
    """创建游戏长度分布图表"""
    # 模拟游戏长度数据
    game_lengths = np.random.normal(35, 8, 1000)  # 示例数据
    game_lengths = np.clip(game_lengths, 20, 50)  # 限制在合理范围内
    
    plt.figure(figsize=(10, 6))
    plt.hist(game_lengths, bins=30, color='#2E8B57', alpha=0.7, edgecolor='black')
    plt.axvline(np.mean(game_lengths), color='red', linestyle='--', linewidth=2, 
                label=f'平均值: {np.mean(game_lengths):.1f}')
    
    plt.xlabel('游戏长度 (移动次数)', fontsize=12)
    plt.ylabel('频次', fontsize=12)
    plt.title('Connect4游戏长度分布', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../../output/connect4_game_lengths.png', dpi=300, bbox_inches='tight')
    plt.show()

def run_connect4_analysis():
    """运行完整的Connect4分析"""
    print("开始Connect4游戏分析...")
    
    simulation = Connect4Simulation()
    
    # 运行模拟
    print("1. Running bot vs random simulation...")
    bot_vs_random = simulation.simulate_bot_vs_random(50, 6)
    
    print("2. Running bot vs bot simulation...")
    bot_vs_bot = simulation.simulate_bot_vs_bot(30, 6, 4)
    
    print("3. Analyzing opening moves...")
opening_analysis = simulation.analyze_opening_moves(50, 6)
    
    print("4. 测试不同深度性能...")
    depth_performance = simulation.performance_vs_depth([2, 4, 6], 20)
    
    # 保存结果
    results = {
        'bot_vs_random': bot_vs_random,
        'bot_vs_bot': bot_vs_bot,
        'opening_analysis': opening_analysis,
        'depth_performance': depth_performance,
        'timestamp': time.strftime('%Y%m%d_%H%M%S')
    }
    
    with open('../../output/connect4_simulation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("分析完成，结果已保存到 connect4_simulation_results.json")
    
    return results

def main():
    """主函数"""
    print("=== Connect4 游戏可视化分析 ===\n")
    
    # 运行分析
    results = run_connect4_analysis()
    
    # 创建可视化图表
    print("\n创建可视化图表...")
    create_connect4_win_rate_chart()
    create_depth_performance_chart()
    create_opening_move_analysis()
    create_game_length_distribution()
    
    print("\n=== 可视化分析完成 ===")

if __name__ == "__main__":
    main() 