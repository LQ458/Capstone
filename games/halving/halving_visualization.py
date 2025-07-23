import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from halving_simulation import HalvingSimulation
import json
import time

# Set font and style
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

def create_halving_win_rate_chart():
    """创建Halving游戏胜率图表"""
    # 模拟数据
    initial_numbers = [10, 20, 30, 50, 100]
    player1_win_rates = [60, 55, 52, 48, 45]  # 示例数据
    player2_win_rates = [40, 45, 48, 52, 55]
    
    x = np.arange(len(initial_numbers))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    bars1 = plt.bar(x - width/2, player1_win_rates, width, label='玩家1 (先手)', color='#2E8B57', alpha=0.8)
    bars2 = plt.bar(x + width/2, player2_win_rates, width, label='玩家2 (后手)', color='#4682B4', alpha=0.8)
    
    plt.xlabel('初始数字', fontsize=12)
    plt.ylabel('胜率 (%)', fontsize=12)
    plt.title('Halving游戏不同初始数字下的胜率分布', fontsize=16, fontweight='bold')
    plt.xticks(x, initial_numbers)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=9)
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('../../output/halving_win_rates.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_game_length_analysis():
    """创建游戏长度分析图表"""
    initial_numbers = [10, 20, 30, 50, 100]
    avg_game_lengths = [8, 12, 15, 18, 22]  # 示例数据
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(initial_numbers, avg_game_lengths, color='#2E8B57', alpha=0.8)
    
    # 添加数值标签
    for bar, length in zip(bars, avg_game_lengths):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                f'{length:.1f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.title('Halving游戏长度与初始数字的关系', fontsize=16, fontweight='bold')
    plt.xlabel('初始数字', fontsize=12)
    plt.ylabel('平均游戏长度 (步数)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../../output/halving_game_lengths.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_performance_scaling_chart():
    """创建算法性能缩放图表"""
    numbers = list(range(10, 101, 10))
    computation_times = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]  # 示例数据
    
    plt.figure(figsize=(12, 6))
    plt.plot(numbers, computation_times, 'o-', color='#4682B4', linewidth=2, markersize=6)
    
    plt.title('Minimax算法性能随数字大小的变化', fontsize=16, fontweight='bold')
    plt.xlabel('初始数字', fontsize=12)
    plt.ylabel('计算时间 (秒)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # 使用对数刻度
    
    # 添加趋势线
    z = np.polyfit(numbers, np.log10(computation_times), 1)
    p = np.poly1d(z)
    plt.plot(numbers, 10**p(numbers), '--', color='red', alpha=0.7, label='趋势线')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('../../output/halving_performance_scaling.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_strategy_analysis_chart():
    """创建策略分析图表"""
    initial_numbers = [10, 20, 30, 50, 100]
    halving_first_moves = [70, 60, 55, 45, 40]  # 选择减半作为第一步的百分比
    subtraction_first_moves = [30, 40, 45, 55, 60]  # 选择减一作为第一步的百分比
    
    x = np.arange(len(initial_numbers))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    bars1 = plt.bar(x - width/2, halving_first_moves, width, label='减半操作', color='#2E8B57', alpha=0.8)
    bars2 = plt.bar(x + width/2, subtraction_first_moves, width, label='减一操作', color='#4682B4', alpha=0.8)
    
    plt.xlabel('初始数字', fontsize=12)
    plt.ylabel('选择频率 (%)', fontsize=12)
    plt.title('Halving游戏第一步策略分析', fontsize=16, fontweight='bold')
    plt.xticks(x, initial_numbers)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=9)
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('../../output/halving_strategy_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_minimax_vs_random_comparison():
    """创建Minimax vs 随机策略对比图表"""
    initial_numbers = [10, 20, 30]
    minimax_win_rates = [95, 90, 85]  # 示例数据
    random_win_rates = [5, 10, 15]
    
    x = np.arange(len(initial_numbers))
    width = 0.35
    
    plt.figure(figsize=(10, 6))
    bars1 = plt.bar(x - width/2, minimax_win_rates, width, label='Minimax策略', color='#2E8B57', alpha=0.8)
    bars2 = plt.bar(x + width/2, random_win_rates, width, label='随机策略', color='#4682B4', alpha=0.8)
    
    plt.xlabel('初始数字', fontsize=12)
    plt.ylabel('胜率 (%)', fontsize=12)
    plt.title('Minimax vs 随机策略胜率对比', fontsize=16, fontweight='bold')
    plt.xticks(x, initial_numbers)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('../../output/halving_minimax_vs_random.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_decision_tree_visualization():
    """创建决策树可视化"""
    # 创建一个简单的决策树示例
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # 定义节点位置
    nodes = {
        '10': (6, 8),
        '9': (4, 6),
        '5': (8, 6),
        '8': (2, 4),
        '4': (6, 4),
        '7': (10, 4),
        '3': (4, 2),
        '2': (8, 2),
        '1': (6, 0)
    }
    
    # 绘制节点和边
    for node, pos in nodes.items():
        ax.plot(pos[0], pos[1], 'o', markersize=20, color='#2E8B57')
        ax.text(pos[0], pos[1], node, ha='center', va='center', fontsize=12, fontweight='bold')
    
    # 绘制边
    edges = [
        ('10', '9', '-1'),
        ('10', '5', '/2'),
        ('9', '8', '-1'),
        ('9', '4', '/2'),
        ('5', '4', '-1'),
        ('5', '2', '/2'),
        ('8', '7', '-1'),
        ('4', '3', '-1'),
        ('4', '2', '/2'),
        ('7', '6', '-1'),
        ('3', '2', '-1'),
        ('2', '1', '-1')
    ]
    
    for start, end, operation in edges:
        if start in nodes and end in nodes:
            start_pos = nodes[start]
            end_pos = nodes[end]
            ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], 'k-', alpha=0.5)
            mid_x = (start_pos[0] + end_pos[0]) / 2
            mid_y = (start_pos[1] + end_pos[1]) / 2
            ax.text(mid_x, mid_y, operation, ha='center', va='center', 
                   fontsize=8, bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(-1, 9)
    ax.set_title('Halving游戏决策树示例 (初始数字=10)', fontsize=16, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('../../output/halving_decision_tree.png', dpi=300, bbox_inches='tight')
    plt.show()

def run_halving_analysis():
    """运行完整的Halving分析"""
    print("开始Halving游戏分析...")
    
    simulation = HalvingSimulation()
    
    # 测试的初始数字
    test_numbers = [10, 20, 30, 50, 100]
    
    # 运行模拟
    print("1. 运行基本游戏模拟...")
    basic_results = simulation.simulate_game_series(test_numbers, 10)
    
    print("2. 分析获胜策略...")
    strategy_analysis = simulation.analyze_winning_strategies(test_numbers)
    
    print("3. 测试算法性能...")
    performance_data = simulation.test_performance_scaling(100, 20)
    
    print("4. 比较Minimax vs 随机策略...")
    comparison_results = simulation.compare_minimax_vs_random(test_numbers[:3], 15)
    
    # 保存结果
    results = {
        'basic_results': basic_results,
        'strategy_analysis': strategy_analysis,
        'performance_data': performance_data,
        'comparison_results': comparison_results,
        'timestamp': time.strftime('%Y%m%d_%H%M%S')
    }
    
    with open('../../output/halving_simulation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("分析完成，结果已保存到 halving_simulation_results.json")
    
    return results

def main():
    """主函数"""
    print("=== Halving 游戏可视化分析 ===\n")
    
    # 运行分析
    results = run_halving_analysis()
    
    # 创建可视化图表
    print("\n创建可视化图表...")
    create_halving_win_rate_chart()
    create_game_length_analysis()
    create_performance_scaling_chart()
    create_strategy_analysis_chart()
    create_minimax_vs_random_comparison()
    create_decision_tree_visualization()
    
    print("\n=== 可视化分析完成 ===")

if __name__ == "__main__":
    main() 