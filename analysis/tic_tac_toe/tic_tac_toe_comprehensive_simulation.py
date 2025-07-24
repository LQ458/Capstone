#!/usr/bin/env python3
"""
Comprehensive Tic-Tac-Toe Simulation Script
Runs real simulations to collect data for visualization
"""

import sys
import os
import json
import time
import random
from datetime import datetime

# Import the TicTacToe game
sys.path.append(os.path.join(os.path.dirname(__file__), '../../games'))
from tic_tac_toe import TicTacToe, PLAYER_X, PLAYER_O, DRAW

class TicTacToeSimulation:
    """Comprehensive simulation class for Tic-Tac-Toe"""
    
    def __init__(self):
        self.results = {}
    
    def simulate_agent_vs_random(self, num_games=100):
        """Simulate agent vs random player (≥100 games)"""
        print(f"Running Agent vs Random simulation ({num_games} games)...")
        
        agent_wins = 0
        random_wins = 0
        draws = 0
        game_lengths = []
        agent_move_times = []
        
        for game_num in range(num_games):
            game = TicTacToe()
            moves = 0
            
            while not game.game_over:
                moves += 1
                
                if game.player == PLAYER_X:  # Agent's turn
                    start_time = time.time()
                    row, col = game.find_best_move()
                    move_time = time.time() - start_time
                    agent_move_times.append(move_time)
                    game.make_move(row, col)
                else:  # Random player's turn
                    available_moves = game.get_available_moves()
                    if available_moves:
                        row, col = random.choice(available_moves)
                        game.make_move(row, col)
            
            game_lengths.append(moves)
            
            if game.winner == PLAYER_X:
                agent_wins += 1
            elif game.winner == PLAYER_O:
                random_wins += 1
            else:
                draws += 1
            
            if (game_num + 1) % 20 == 0:
                print(f"  Completed {game_num + 1}/{num_games} games")
        
        results = {
            'agent_wins': agent_wins,
            'random_wins': random_wins,
            'draws': draws,
            'total_games': num_games,
            'agent_win_rate': (agent_wins / num_games) * 100,
            'random_win_rate': (random_wins / num_games) * 100,
            'draw_rate': (draws / num_games) * 100,
            'avg_game_length': sum(game_lengths) / len(game_lengths),
            'avg_agent_move_time': sum(agent_move_times) / len(agent_move_times) if agent_move_times else 0,
            'game_lengths': game_lengths
        }
        
        print(f"  Agent win rate: {results['agent_win_rate']:.1f}%")
        print(f"  Random win rate: {results['random_win_rate']:.1f}%")
        print(f"  Draw rate: {results['draw_rate']:.1f}%")
        print(f"  Average game length: {results['avg_game_length']:.1f} moves")
        
        return results
    
    def simulate_agent_vs_agent(self, num_games=100):
        """Simulate agent vs agent games"""
        print(f"Running Agent vs Agent simulation ({num_games} games)...")
        
        x_wins = 0
        o_wins = 0
        draws = 0
        game_lengths = []
        total_computation_time = 0
        
        for game_num in range(num_games):
            game = TicTacToe()
            moves = 0
            game_start_time = time.time()
            
            while not game.game_over:
                moves += 1
                row, col = game.find_best_move()
                game.make_move(row, col)
            
            total_computation_time += time.time() - game_start_time
            game_lengths.append(moves)
            
            if game.winner == PLAYER_X:
                x_wins += 1
            elif game.winner == PLAYER_O:
                o_wins += 1
            else:
                draws += 1
            
            if (game_num + 1) % 20 == 0:
                print(f"  Completed {game_num + 1}/{num_games} games")
        
        results = {
            'x_wins': x_wins,
            'o_wins': o_wins,
            'draws': draws,
            'total_games': num_games,
            'x_win_rate': (x_wins / num_games) * 100,
            'o_win_rate': (o_wins / num_games) * 100,
            'draw_rate': (draws / num_games) * 100,
            'avg_game_length': sum(game_lengths) / len(game_lengths),
            'avg_computation_time': total_computation_time / num_games,
            'game_lengths': game_lengths
        }
        
        print(f"  X (first player) win rate: {results['x_win_rate']:.1f}%")
        print(f"  O (second player) win rate: {results['o_win_rate']:.1f}%")
        print(f"  Draw rate: {results['draw_rate']:.1f}%")
        print(f"  Average game length: {results['avg_game_length']:.1f} moves")
        
        return results
    
    def test_search_depth_performance(self, depths=[1, 2, 3, 4, 5, 6], games_per_depth=50):
        """Test performance at different search depths (modified minimax for depth testing)"""
        print(f"Testing search depth performance...")
        
        depth_results = {}
        
        for depth in depths:
            print(f"  Testing depth {depth}...")
            
            agent_wins = 0
            random_wins = 0
            draws = 0
            move_times = []
            
            for game_num in range(games_per_depth):
                game = TicTacToe()
                
                while not game.game_over:
                    if game.player == PLAYER_X:  # Agent with limited depth
                        start_time = time.time()
                        row, col = self.find_best_move_with_depth(game, depth)
                        move_time = time.time() - start_time
                        move_times.append(move_time)
                        game.make_move(row, col)
                    else:  # Random player
                        available_moves = game.get_available_moves()
                        if available_moves:
                            row, col = random.choice(available_moves)
                            game.make_move(row, col)
                
                if game.winner == PLAYER_X:
                    agent_wins += 1
                elif game.winner == PLAYER_O:
                    random_wins += 1
                else:
                    draws += 1
            
            depth_results[depth] = {
                'agent_wins': agent_wins,
                'random_wins': random_wins,
                'draws': draws,
                'agent_win_rate': (agent_wins / games_per_depth) * 100,
                'avg_move_time': sum(move_times) / len(move_times) if move_times else 0,
                'total_games': games_per_depth
            }
            
            print(f"    Depth {depth}: {depth_results[depth]['agent_win_rate']:.1f}% win rate, {depth_results[depth]['avg_move_time']:.4f}s avg time")
        
        return depth_results
    
    def find_best_move_with_depth(self, game, max_depth):
        """Find best move with limited search depth"""
        if game.cnt == 0 and game.board[1][1] == 0:  # First move, take center
            return (1, 1)
        
        best_val = float('-inf') if game.player == PLAYER_X else float('inf')
        best_move = (-1, -1)
        
        for i in range(3):
            for j in range(3):
                if game.board[i][j] == 0:  # Empty cell
                    game.board[i][j] = game.player
                    move_val = self.minimax_with_depth(game, 0, max_depth, game.player == PLAYER_O)
                    game.board[i][j] = 0  # Undo move
                    
                    if game.player == PLAYER_X:
                        if move_val > best_val:
                            best_move = (i, j)
                            best_val = move_val
                    else:
                        if move_val < best_val:
                            best_move = (i, j)
                            best_val = move_val
        
        return best_move
    
    def minimax_with_depth(self, game, depth, max_depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        """Minimax with depth limit"""
        score = game.evaluate_board()
        
        # Terminal state or depth limit reached
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if len(game.get_available_moves()) == 0:
            return 0
        if depth >= max_depth:
            return 0  # Neutral evaluation at depth limit
        
        if is_maximizing:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if game.board[i][j] == 0:
                        game.board[i][j] = PLAYER_X
                        best = max(best, self.minimax_with_depth(game, depth + 1, max_depth, False, alpha, beta))
                        game.board[i][j] = 0
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if game.board[i][j] == 0:
                        game.board[i][j] = PLAYER_O
                        best = min(best, self.minimax_with_depth(game, depth + 1, max_depth, True, alpha, beta))
                        game.board[i][j] = 0
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best
    
    def analyze_opening_moves(self, num_games=100):
        """Analyze opening move preferences"""
        print(f"Analyzing opening move preferences ({num_games} games)...")
        
        opening_moves = {
            'agent': [],
            'random': []
        }
        
        for game_num in range(num_games):
            game = TicTacToe()
            
            # Agent's opening move (always X, goes first)
            row, col = game.find_best_move()
            opening_moves['agent'].append((row, col))
            game.make_move(row, col)
            
            # Random opponent's opening move
            if not game.game_over:
                available_moves = game.get_available_moves()
                if available_moves:
                    row, col = random.choice(available_moves)
                    opening_moves['random'].append((row, col))
        
        # Calculate distributions
        opening_distribution = {}
        for player in ['agent', 'random']:
            opening_distribution[player] = {}
            for row in range(3):
                for col in range(3):
                    count = opening_moves[player].count((row, col))
                    opening_distribution[player][f"({row},{col})"] = {
                        'count': count,
                        'percentage': (count / len(opening_moves[player])) * 100 if opening_moves[player] else 0
                    }
        
        return opening_distribution
    
    def run_comprehensive_simulation(self):
        """Run all simulations and collect comprehensive data"""
        print("=" * 60)
        print("COMPREHENSIVE TIC-TAC-TOE SIMULATION")
        print("=" * 60)
        
        start_time = time.time()
        
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'game': 'Tic-Tac-Toe',
            'simulation_results': {}
        }
        
        # 1. Agent vs Random (≥100 games)
        print("\n1. AGENT VS RANDOM SIMULATION")
        print("-" * 40)
        agent_vs_random = self.simulate_agent_vs_random(150)
        self.results['simulation_results']['agent_vs_random'] = agent_vs_random
        
        # 2. Agent vs Agent
        print("\n2. AGENT VS AGENT SIMULATION")
        print("-" * 40)
        agent_vs_agent = self.simulate_agent_vs_agent(100)
        self.results['simulation_results']['agent_vs_agent'] = agent_vs_agent
        
        # 3. Search depth performance
        print("\n3. SEARCH DEPTH PERFORMANCE")
        print("-" * 40)
        depth_performance = self.test_search_depth_performance([1, 2, 3, 4, 5, 6], 50)
        self.results['simulation_results']['depth_performance'] = depth_performance
        
        # 4. Opening move analysis
        print("\n4. OPENING MOVE ANALYSIS")
        print("-" * 40)
        opening_analysis = self.analyze_opening_moves(100)
        self.results['simulation_results']['opening_analysis'] = opening_analysis
        
        # Print opening move summary
        agent_opening = opening_analysis['agent']
        most_common_opening = max(agent_opening.items(), key=lambda x: x[1]['count'])
        print(f"  Most common agent opening: {most_common_opening[0]} ({most_common_opening[1]['percentage']:.1f}%)")
        
        # 5. Performance metrics
        total_time = time.time() - start_time
        total_games = (150 + 100 + 6*50 + 100)  # Sum of all games
        
        self.results['simulation_results']['performance_metrics'] = {
            'total_simulation_time': total_time,
            'total_games_simulated': total_games,
            'games_per_second': total_games / total_time,
            'avg_time_per_game': total_time / total_games
        }
        
        # Save results to JSON
        output_dir = '../../output/text'
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f'tic_tac_toe_comprehensive_results_{timestamp}.json')
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print("\n" + "=" * 60)
        print("TIC-TAC-TOE SIMULATION COMPLETE")
        print("=" * 60)
        print(f"Total games simulated: {total_games}")
        print(f"Total time: {total_time:.1f} seconds")
        print(f"Games per second: {total_games / total_time:.1f}")
        print(f"Results saved to: {filename}")
        
        return self.results, filename

def main():
    """Main function to run the comprehensive simulation"""
    simulation = TicTacToeSimulation()
    results, filename = simulation.run_comprehensive_simulation()
    
    print(f"\nSimulation data saved to: {filename}")
    print("This data can now be used by visualization scripts.")

if __name__ == "__main__":
    main()