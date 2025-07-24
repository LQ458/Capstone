import random
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../games'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../games/connect4'))
from connect4 import ConnectFour
import test as c4f

class Connect4Simulation:
    """
    Connect4 game simulation class for AI battles and performance analysis
    """
    
    def __init__(self):
        self.game = ConnectFour()
        self.results = []
        
    def simulate_ai_vs_random(self, num_games=100, ai_depth=8):
        """AI vs random player simulation"""
        print(f"Starting AI vs random player simulation, {num_games} games total...")
        
        ai_wins = 0
        random_wins = 0
        draws = 0
        total_moves = 0
        ai_move_times = []
        
        for game_num in range(num_games):
            self.game = ConnectFour()
            moves = 0
            
            while True:
                if self.game.current_player == 'X':  # AI player
                    start_time = time.time()
                    col = self.game.best_move(ai_depth)
                    move_time = time.time() - start_time
                    ai_move_times.append(move_time)
                    self.game.make_move(col)
                else:  # Random player
                    valid_moves = self.game.get_valid_moves()
                    if valid_moves:
                        col = random.choice(valid_moves)
                        self.game.make_move(col)
                    else:
                        break
                
                moves += 1
                
                # Check if game is over
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
                print(f"Completed {game_num + 1}/{num_games} games")
        
        results = {
            'ai_wins': ai_wins,
            'random_wins': random_wins,
            'draws': draws,
            'total_games': num_games,
            'avg_moves': total_moves / num_games,
            'avg_ai_move_time': sum(ai_move_times) / len(ai_move_times) if ai_move_times else 0,
            'ai_win_rate': (ai_wins / num_games) * 100
        }
        
        print(f"AI win rate: {results['ai_win_rate']:.1f}%")
        print(f"Average moves per game: {results['avg_moves']:.1f}")
        print(f"AI average thinking time: {results['avg_ai_move_time']:.3f} seconds")
        
        return results
    
    def simulate_ai_vs_ai(self, num_games=50, depth1=8, depth2=6):
        """Two AIs with different depths battle"""
        print(f"Starting AI vs AI simulation, depth {depth1} vs depth {depth2}, {num_games} games total...")
        
        ai1_wins = 0
        ai2_wins = 0
        draws = 0
        total_moves = 0
        
        for game_num in range(num_games):
            self.game = ConnectFour()
            moves = 0
            
            while True:
                if self.game.current_player == 'X':  # AI1 (deeper depth)
                    col = self.game.best_move(depth1)
                else:  # AI2 (shallower depth)
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
                print(f"Completed {game_num + 1}/{num_games} games")
        
        results = {
            'ai1_wins': ai1_wins,
            'ai2_wins': ai2_wins,
            'draws': draws,
            'total_games': num_games,
            'avg_moves': total_moves / num_games,
            'ai1_win_rate': (ai1_wins / num_games) * 100,
            'ai2_win_rate': (ai2_wins / num_games) * 100
        }
        
        print(f"Depth {depth1} AI win rate: {results['ai1_win_rate']:.1f}%")
        print(f"Depth {depth2} AI win rate: {results['ai2_win_rate']:.1f}%")
        print(f"Average moves per game: {results['avg_moves']:.1f}")
        
        return results
    
    def analyze_opening_moves(self, num_games=100, ai_depth=8):
        """Analyze the distribution of opening moves"""
        print(f"Analyzing opening move distribution, {num_games} games total...")
        
        opening_moves = {'X': [], 'O': []}
        
        for game_num in range(num_games):
            self.game = ConnectFour()
            
            # Record AI's opening move
            if self.game.current_player == 'X':
                col = self.game.best_move(ai_depth)
                opening_moves['X'].append(col)
            else:
                # Random opponent's opening move
                col = random.choice(self.game.get_valid_moves())
                opening_moves['O'].append(col)
        
        # Calculate move distribution
        move_distribution = {}
        for player in ['X', 'O']:
            move_distribution[player] = {}
            for col in range(7):
                count = opening_moves[player].count(col)
                move_distribution[player][col] = (count / num_games) * 100
        
        return move_distribution
    
    def performance_vs_depth(self, depths=[2, 4, 6, 8], games_per_depth=50):
        """Test performance at different search depths"""
        print("Testing performance at different search depths...")
        
        results = {}
        
        for depth in depths:
            print(f"Testing depth {depth}...")
            start_time = time.time()
            
            # Run AI vs random player test
            depth_results = self.simulate_ai_vs_random(games_per_depth, depth)
            depth_results['depth'] = depth
            depth_results['total_time'] = time.time() - start_time
            
            results[depth] = depth_results
        
        return results

def main():
    """Main function to run various simulations"""
    simulation = Connect4Simulation()
    
    print("=== Connect4 Game Simulation Analysis ===\n")
    
    # 1. AI vs Random Player
    print("1. AI vs Random Player Analysis")
    ai_vs_random = simulation.simulate_ai_vs_random(100, 8)
    print()
    
    # 2. AI vs AI
    print("2. AI vs AI Analysis")
    ai_vs_ai = simulation.simulate_ai_vs_ai(50, 8, 6)
    print()
    
    # 3. Opening Move Analysis
    print("3. Opening Move Distribution Analysis")
    opening_analysis = simulation.analyze_opening_moves(100, 8)
    for player, moves in opening_analysis.items():
        print(f"{player} player opening move distribution:")
        for col, percentage in moves.items():
            print(f"  Column {col}: {percentage:.1f}%")
    print()
    
    # 4. Depth Performance Analysis
    print("4. Search Depth Performance Analysis")
    depth_performance = simulation.performance_vs_depth([2, 4, 6, 8], 30)
    for depth, results in depth_performance.items():
        print(f"Depth {depth}: Win rate {results['ai_win_rate']:.1f}%, Avg time {results['avg_ai_move_time']:.3f}s")
    
    print("\n=== Simulation Complete ===")

if __name__ == "__main__":
    main() 