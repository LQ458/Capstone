import random
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connect4 import ConnectFour
import test as c4f

class Connect4Simulation:
    """
    Connect4游戏模拟类，用于进行AI对战和性能分析
    """
    
    def __init__(self):
        self.game = ConnectFour()
        self.results = []
        
    def simulate_ai_vs_random(self, num_games=100, ai_depth=6):
        """AI对战随机玩家的模拟"""
        print(f"开始AI对战随机玩家模拟，共{num_games}局游戏...")
        
        ai_wins = 0
        random_wins = 0
        draws = 0
        total_moves = 0
        ai_move_times = []
        
        for game_num in range(num_games):
            self.game = ConnectFour()
            moves = 0
            
            while True:
                if self.game.current_player == 'X':  # AI玩家
                    start_time = time.time()
                    col = self.game.best_move(ai_depth)
                    move_time = time.time() - start_time
                    ai_move_times.append(move_time)
                    self.game.make_move(col)
                else:  # 随机玩家
                    valid_moves = self.game.get_valid_moves()
                    if valid_moves:
                        col = random.choice(valid_moves)
                        self.game.make_move(col)
                    else:
                        break
                
                moves += 1
                
                # 检查游戏是否结束
                if c4f.win(self.game.bitboard['X']):
                    ai_wins += 1
                    break
                elif c4f.win(self.game.bitboard['O']):
                    random_wins += 1
                    break
                elif not self.game.get_valid_moves():
                    draws += 1
                    break
            
            total_moves += moves
            
            if (game_num + 1) % 20 == 0:
                print(f"已完成 {game_num + 1}/{num_games} 局游戏")
        
        results = {
            'ai_wins': ai_wins,
            'random_wins': random_wins,
            'draws': draws,
            'total_games': num_games,
            'avg_moves': total_moves / num_games,
            'avg_ai_move_time': sum(ai_move_times) / len(ai_move_times) if ai_move_times else 0,
            'ai_win_rate': (ai_wins / num_games) * 100
        }
        
        print(f"AI胜率: {results['ai_win_rate']:.1f}%")
        print(f"平均每局移动数: {results['avg_moves']:.1f}")
        print(f"AI平均思考时间: {results['avg_ai_move_time']:.3f}秒")
        
        return results
    
    def simulate_ai_vs_ai(self, num_games=50, depth1=6, depth2=4):
        """两个不同深度的AI对战"""
        print(f"开始AI对战AI模拟，深度{depth1} vs 深度{depth2}，共{num_games}局游戏...")
        
        ai1_wins = 0
        ai2_wins = 0
        draws = 0
        total_moves = 0
        
        for game_num in range(num_games):
            self.game = ConnectFour()
            moves = 0
            
            while True:
                if self.game.current_player == 'X':  # AI1 (深度更深)
                    col = self.game.best_move(depth1)
                else:  # AI2 (深度较浅)
                    col = self.game.best_move(depth2)
                
                self.game.make_move(col)
                moves += 1
                
                # 检查游戏是否结束
                if c4f.win(self.game.bitboard['X']):
                    ai1_wins += 1
                    break
                elif c4f.win(self.game.bitboard['O']):
                    ai2_wins += 1
                    break
                elif not self.game.get_valid_moves():
                    draws += 1
                    break
            
            total_moves += moves
            
            if (game_num + 1) % 10 == 0:
                print(f"已完成 {game_num + 1}/{num_games} 局游戏")
        
        results = {
            'ai1_wins': ai1_wins,
            'ai2_wins': ai2_wins,
            'draws': draws,
            'total_games': num_games,
            'avg_moves': total_moves / num_games,
            'ai1_win_rate': (ai1_wins / num_games) * 100,
            'ai2_win_rate': (ai2_wins / num_games) * 100
        }
        
        print(f"深度{depth1} AI胜率: {results['ai1_win_rate']:.1f}%")
        print(f"深度{depth2} AI胜率: {results['ai2_win_rate']:.1f}%")
        print(f"平均每局移动数: {results['avg_moves']:.1f}")
        
        return results
    
    def analyze_opening_moves(self, num_games=100, ai_depth=6):
        """分析开局移动的分布"""
        print(f"分析开局移动分布，共{num_games}局游戏...")
        
        opening_moves = {'X': [], 'O': []}
        
        for game_num in range(num_games):
            self.game = ConnectFour()
            
            # 记录AI的开局移动
            if self.game.current_player == 'X':
                col = self.game.best_move(ai_depth)
                opening_moves['X'].append(col)
            else:
                # 随机对手的开局移动
                col = random.choice(self.game.get_valid_moves())
                opening_moves['O'].append(col)
        
        # 统计移动分布
        move_distribution = {}
        for player in ['X', 'O']:
            move_distribution[player] = {}
            for col in range(7):
                count = opening_moves[player].count(col)
                move_distribution[player][col] = (count / num_games) * 100
        
        return move_distribution
    
    def performance_vs_depth(self, depths=[2, 4, 6, 8], games_per_depth=50):
        """测试不同深度下的性能表现"""
        print("测试不同搜索深度下的性能表现...")
        
        results = {}
        
        for depth in depths:
            print(f"测试深度 {depth}...")
            start_time = time.time()
            
            # 进行AI对战随机玩家的测试
            depth_results = self.simulate_ai_vs_random(games_per_depth, depth)
            depth_results['depth'] = depth
            depth_results['total_time'] = time.time() - start_time
            
            results[depth] = depth_results
        
        return results

def main():
    """主函数，运行各种模拟"""
    simulation = Connect4Simulation()
    
    print("=== Connect4 游戏模拟分析 ===\n")
    
    # 1. AI对战随机玩家
    print("1. AI对战随机玩家分析")
    ai_vs_random = simulation.simulate_ai_vs_random(100, 6)
    print()
    
    # 2. AI对战AI
    print("2. AI对战AI分析")
    ai_vs_ai = simulation.simulate_ai_vs_ai(50, 6, 4)
    print()
    
    # 3. 开局移动分析
    print("3. 开局移动分布分析")
    opening_analysis = simulation.analyze_opening_moves(100, 6)
    for player, moves in opening_analysis.items():
        print(f"{player}玩家开局移动分布:")
        for col, percentage in moves.items():
            print(f"  列{col}: {percentage:.1f}%")
    print()
    
    # 4. 深度性能分析
    print("4. 搜索深度性能分析")
    depth_performance = simulation.performance_vs_depth([2, 4, 6], 30)
    for depth, results in depth_performance.items():
        print(f"深度{depth}: 胜率{results['ai_win_rate']:.1f}%, 平均时间{results['avg_ai_move_time']:.3f}秒")
    
    print("\n=== 模拟完成 ===")

if __name__ == "__main__":
    main() 