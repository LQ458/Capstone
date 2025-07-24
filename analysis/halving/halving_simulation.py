import random
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../games'))
from Halving import HalvingGame

class HalvingSimulation:
    """
    Halving游戏模拟类，用于进行策略分析和性能测试
    """
    
    def __init__(self):
        self.results = []
        
    def simulate_game_series(self, initial_numbers, num_games_per_number=10):
        """对多个初始数字进行游戏模拟"""
        print(f"开始Halving游戏系列模拟，测试{len(initial_numbers)}个初始数字...")
        
        all_results = {}
        
        for initial_num in initial_numbers:
            print(f"\n测试初始数字: {initial_num}")
            results = self.simulate_single_number(initial_num, num_games_per_number)
            all_results[initial_num] = results
        
        return all_results
    
    def simulate_single_number(self, initial_number, num_games=10):
        """Simulate multiple games for a single initial number"""
        player1_wins = 0
        player2_wins = 0
        game_lengths = []
        move_sequences = []
        
        for game_num in range(num_games):
            game = HalvingGame(initial_number)
            current_number = initial_number
            current_player = 1
            moves = []
            
            while current_number > 1:
                is_maximizing = (current_player == 1)
                _, move = game.minimax(current_number, is_maximizing)
                
                operation = "-1" if move == current_number - 1 else "/2"
                moves.append({
                    'player': current_player,
                    'from': current_number,
                    'to': move,
                    'operation': operation
                })
                
                current_number = move
                current_player = 2 if current_player == 1 else 1
            
            # 确定获胜者
            winner = 2 if current_player == 1 else 1
            if winner == 1:
                player1_wins += 1
            else:
                player2_wins += 1
            
            game_lengths.append(len(moves))
            move_sequences.append(moves)
            
            if (game_num + 1) % 5 == 0:
                print(f"  Completed {game_num + 1}/{num_games} games")
        
        results = {
            'initial_number': initial_number,
            'player1_wins': player1_wins,
            'player2_wins': player2_wins,
            'total_games': num_games,
            'avg_game_length': sum(game_lengths) / len(game_lengths),
            'player1_win_rate': (player1_wins / num_games) * 100,
            'player2_win_rate': (player2_wins / num_games) * 100,
            'move_sequences': move_sequences
        }
        
        print(f"  Player 1 win rate: {results['player1_win_rate']:.1f}%")
        print(f"  Player 2 win rate: {results['player2_win_rate']:.1f}%")
        print(f"  Average game length: {results['avg_game_length']:.1f} moves")
        
        return results
    
    def analyze_winning_strategies(self, initial_numbers):
        """分析获胜策略"""
        print("分析获胜策略...")
        
        strategy_analysis = {}
        
        for initial_num in initial_numbers:
            print(f"\n分析初始数字 {initial_num} 的策略:")
            game = HalvingGame(initial_num)
            
            # 分析第一步的最佳移动
            _, first_move = game.minimax(initial_num, True)
            first_operation = "-1" if first_move == initial_num - 1 else "/2"
            
            # 分析游戏的关键决策点
            key_decisions = []
            current_num = initial_num
            player = 1
            
            while current_num > 1:
                is_maximizing = (player == 1)
                _, move = game.minimax(current_num, is_maximizing)
                
                # 检查是否有多个选择
                possible_moves = game.get_moves(current_num)
                if len(possible_moves) > 1:
                    # 分析每个选择的后果
                    move_analysis = {}
                    for possible_move in possible_moves:
                        # 模拟对手的最佳回应
                        _, opponent_move = game.minimax(possible_move, not is_maximizing)
                        move_analysis[possible_move] = {
                            'operation': "-1" if possible_move == current_num - 1 else "/2",
                            'next_state': opponent_move
                        }
                    
                    key_decisions.append({
                        'number': current_num,
                        'player': player,
                        'chosen_move': move,
                        'all_moves': move_analysis
                    })
                
                current_num = move
                player = 2 if player == 1 else 1
            
            strategy_analysis[initial_num] = {
                'first_move': first_move,
                'first_operation': first_operation,
                'key_decisions': key_decisions
            }
            
            print(f"  第一步最佳移动: {initial_num} {first_operation} => {first_move}")
            print(f"  关键决策点数量: {len(key_decisions)}")
        
        return strategy_analysis
    
    def test_performance_scaling(self, max_number=100, step=10):
        """测试算法性能随数字大小的变化"""
        print("测试算法性能随数字大小的变化...")
        
        performance_data = []
        
        for num in range(10, max_number + 1, step):
            print(f"测试数字: {num}")
            game = HalvingGame(num)
            
            start_time = time.time()
            _, _ = game.minimax(num, True)
            computation_time = time.time() - start_time
            
            performance_data.append({
                'number': num,
                'computation_time': computation_time
            })
            
            print(f"  计算时间: {computation_time:.3f}秒")
        
        return performance_data
    
    def compare_minimax_vs_random(self, initial_numbers, num_games=20):
        """比较Minimax算法与随机策略"""
        print("比较Minimax算法与随机策略...")
        
        comparison_results = {}
        
        for initial_num in initial_numbers:
            print(f"\n比较初始数字 {initial_num}:")
            
            # Minimax vs Minimax
            minimax_results = self.simulate_single_number(initial_num, num_games)
            
            # Minimax vs Random
            minimax_vs_random = self.simulate_minimax_vs_random(initial_num, num_games)
            
            comparison_results[initial_num] = {
                'minimax_vs_minimax': minimax_results,
                'minimax_vs_random': minimax_vs_random
            }
            
            print(f"  Minimax vs Minimax - 玩家1胜率: {minimax_results['player1_win_rate']:.1f}%")
            print(f"  Minimax vs Random - Minimax胜率: {minimax_vs_random['minimax_win_rate']:.1f}%")
        
        return comparison_results
    
    def simulate_minimax_vs_random(self, initial_number, num_games=20):
        """Minimax算法对战随机策略"""
        minimax_wins = 0
        random_wins = 0
        game_lengths = []
        
        for game_num in range(num_games):
            game = HalvingGame(initial_number)
            current_number = initial_number
            current_player = 1  # Minimax玩家
            
            while current_number > 1:
                if current_player == 1:  # Minimax玩家
                    _, move = game.minimax(current_number, True)
                else:  # 随机玩家
                    possible_moves = game.get_moves(current_number)
                    move = random.choice(possible_moves)
                
                current_number = move
                current_player = 2 if current_player == 1 else 1
            
            # 确定获胜者
            winner = 2 if current_player == 1 else 1
            if winner == 1:  # Minimax玩家获胜
                minimax_wins += 1
            else:
                random_wins += 1
            
            game_lengths.append(moves)
        
        return {
            'minimax_wins': minimax_wins,
            'random_wins': random_wins,
            'total_games': num_games,
            'minimax_win_rate': (minimax_wins / num_games) * 100,
            'avg_game_length': sum(game_lengths) / len(game_lengths)
        }

def main():
    """主函数，运行各种模拟"""
    simulation = HalvingSimulation()
    
    print("=== Halving 游戏模拟分析 ===\n")
    
    # 测试的初始数字
    test_numbers = [10, 20, 30, 50, 100]
    
    # 1. 基本游戏模拟
    print("1. 基本游戏模拟")
    basic_results = simulation.simulate_game_series(test_numbers, 10)
    print()
    
    # 2. 策略分析
    print("2. 获胜策略分析")
    strategy_analysis = simulation.analyze_winning_strategies(test_numbers)
    print()
    
    # 3. 性能测试
    print("3. 算法性能测试")
    performance_data = simulation.test_performance_scaling(100, 20)
    print()
    
    # 4. 策略比较
    print("4. Minimax vs 随机策略比较")
    comparison_results = simulation.compare_minimax_vs_random(test_numbers[:3], 15)
    print()
    
    # 输出总结
    print("=== 模拟结果总结 ===")
    for num in test_numbers:
        if num in basic_results:
            results = basic_results[num]
            print(f"初始数字 {num}:")
            print(f"  玩家1胜率: {results['player1_win_rate']:.1f}%")
            print(f"  平均游戏长度: {results['avg_game_length']:.1f}步")
    
    print("\n=== 模拟完成 ===")

if __name__ == "__main__":
    main() 