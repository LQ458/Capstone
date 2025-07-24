#!/usr/bin/env python3
"""
Comprehensive Connect4 Simulation Script
Runs real simulations to collect data for visualization
"""

import sys
import os
import json
import time
import random
from datetime import datetime

# Import the Connect4 game
sys.path.append(os.path.join(os.path.dirname(__file__), '../../games/connect4'))
from connect4 import ConnectFour
import test as c4f

class Connect4ComprehensiveSimulation:
    """Enhanced simulation class for Connect4"""
    
    def __init__(self):
        self.results = {}
    
    def simulate_ai_vs_random_depth_analysis(self, depths=[2, 4, 6, 8, 10], games_per_depth=50):
        """Simulate AI vs random at different depths"""
        print(f"Running AI vs Random at different depths...")
        
        depth_results = {}
        
        for depth in depths:
            print(f"  Testing depth {depth}...")
            
            ai_wins = 0
            random_wins = 0
            draws = 0
            total_moves = 0
            ai_move_times = []
            
            for game_num in range(games_per_depth):
                game = ConnectFour()
                moves = 0
                
                while True:
                    if game.current_player == 'X':  # AI player
                        start_time = time.time()
                        col = game.best_move(depth)
                        move_time = time.time() - start_time
                        ai_move_times.append(move_time)
                        game.make_move(col)
                    else:  # Random player
                        valid_moves = game.get_valid_moves()
                        if valid_moves:
                            col = random.choice(valid_moves)
                            game.make_move(col)
                        else:
                            break
                    
                    moves += 1
                    
                    # Check if game is over
                    if c4f.win(game.bitboard['X']):
                        ai_wins += 1
                        break
                    elif c4f.win(game.bitboard['O']):
                        random_wins += 1
                        break
                    elif not game.get_valid_moves():
                        draws += 1
                        break
                
                total_moves += moves
            
            depth_results[depth] = {
                'ai_wins': ai_wins,
                'random_wins': random_wins,
                'draws': draws,
                'total_games': games_per_depth,
                'ai_win_rate': (ai_wins / games_per_depth) * 100,
                'avg_moves': total_moves / games_per_depth,
                'avg_ai_move_time': sum(ai_move_times) / len(ai_move_times) if ai_move_times else 0,
                'total_ai_time': sum(ai_move_times),
                'depth': depth
            }
            
            print(f"    Depth {depth}: {depth_results[depth]['ai_win_rate']:.1f}% win rate, {depth_results[depth]['avg_ai_move_time']:.4f}s avg time")
        
        return depth_results
    
    def simulate_ai_vs_ai_comparison(self, depth_pairs=[(8, 6), (8, 4), (6, 4), (8, 2)], games_per_pair=50):
        """AI vs AI with different depths"""
        print(f"Running AI vs AI depth comparisons...")
        
        comparison_results = {}
        
        for depth1, depth2 in depth_pairs:
            print(f"  Testing depth {depth1} vs depth {depth2}...")
            
            ai1_wins = 0
            ai2_wins = 0
            draws = 0
            total_moves = 0
            ai1_times = []
            ai2_times = []
            
            for game_num in range(games_per_pair):
                game = ConnectFour()
                moves = 0
                
                while True:
                    if game.current_player == 'X':  # AI1 (deeper depth)
                        start_time = time.time()
                        col = game.best_move(depth1)
                        move_time = time.time() - start_time
                        ai1_times.append(move_time)
                        game.make_move(col)
                    else:  # AI2 (shallower depth)
                        start_time = time.time()
                        col = game.best_move(depth2)
                        move_time = time.time() - start_time
                        ai2_times.append(move_time)
                        game.make_move(col)
                    
                    moves += 1
                    
                    # Check if game is over
                    if c4f.win(game.bitboard['X']):
                        ai1_wins += 1
                        break
                    elif c4f.win(game.bitboard['O']):
                        ai2_wins += 1
                        break
                    elif not game.get_valid_moves():
                        draws += 1
                        break
                
                total_moves += moves
            
            comparison_results[f"{depth1}_vs_{depth2}"] = {
                'ai1_wins': ai1_wins,
                'ai2_wins': ai2_wins,
                'draws': draws,
                'total_games': games_per_pair,
                'ai1_win_rate': (ai1_wins / games_per_pair) * 100,
                'ai2_win_rate': (ai2_wins / games_per_pair) * 100,
                'draw_rate': (draws / games_per_pair) * 100,
                'avg_moves': total_moves / games_per_pair,
                'ai1_avg_time': sum(ai1_times) / len(ai1_times) if ai1_times else 0,
                'ai2_avg_time': sum(ai2_times) / len(ai2_times) if ai2_times else 0,
                'depth1': depth1,
                'depth2': depth2
            }
            
            result = comparison_results[f"{depth1}_vs_{depth2}"]
            print(f"    Depth {depth1}: {result['ai1_win_rate']:.1f}% win rate")
            print(f"    Depth {depth2}: {result['ai2_win_rate']:.1f}% win rate")
            print(f"    Draws: {result['draw_rate']:.1f}%")
        
        return comparison_results
    
    def analyze_opening_move_preferences(self, depth=8, num_games=100):
        """Analyze opening move preferences for different players"""
        print(f"Analyzing opening move preferences ({num_games} games)...")
        
        opening_moves = {
            'X': [],  # First player (AI)
            'O': []   # Second player (AI or random)
        }
        
        # AI first moves
        for game_num in range(num_games):
            game = ConnectFour()
            
            # Record AI's opening move
            if game.current_player == 'X':
                col = game.best_move(depth)
                opening_moves['X'].append(col)
                game.make_move(col)
                
                # AI's response to opening
                if not c4f.win(game.bitboard['X']) and game.get_valid_moves():
                    col = game.best_move(depth)
                    opening_moves['O'].append(col)
        
        # Calculate move distributions
        move_distribution = {}
        for player in ['X', 'O']:
            move_distribution[player] = {}
            total_moves = len(opening_moves[player])
            for col in range(7):
                count = opening_moves[player].count(col)
                move_distribution[player][col] = {
                    'count': count,
                    'percentage': (count / total_moves) * 100 if total_moves > 0 else 0
                }
        
        return move_distribution
    
    def test_computation_time_scaling(self, depths=[2, 4, 6, 8, 10, 12], positions_per_depth=20):
        """Test how computation time scales with search depth"""
        print(f"Testing computation time scaling...")
        
        timing_results = {}
        
        for depth in depths:
            print(f"  Testing depth {depth}...")
            
            times = []
            
            for _ in range(positions_per_depth):
                game = ConnectFour()
                
                # Make a few random moves to get to mid-game position
                for _ in range(random.randint(3, 10)):
                    valid_moves = game.get_valid_moves()
                    if valid_moves:
                        col = random.choice(valid_moves)
                        game.make_move(col)
                    if c4f.win(game.bitboard['X']) or c4f.win(game.bitboard['O']) or not game.get_valid_moves():
                        break
                
                # Time the AI move
                if game.get_valid_moves() and not c4f.win(game.bitboard['X']) and not c4f.win(game.bitboard['O']):
                    start_time = time.time()
                    game.best_move(depth)
                    move_time = time.time() - start_time
                    times.append(move_time)
            
            if times:
                timing_results[depth] = {
                    'avg_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times),
                    'total_positions': len(times),
                    'depth': depth
                }
                
                print(f"    Depth {depth}: {timing_results[depth]['avg_time']:.4f}s avg time")
        
        return timing_results
    
    def simulate_win_rate_vs_random(self, num_games=100, depth=8):
        """Detailed win rate analysis vs random player"""
        print(f"Running detailed win rate analysis vs random ({num_games} games)...")
        
        results = {
            'ai_wins': 0,
            'random_wins': 0,
            'draws': 0,
            'games': [],
            'move_times': [],
            'game_lengths': []
        }
        
        for game_num in range(num_games):
            game = ConnectFour()
            moves = 0
            game_moves = []
            game_times = []
            
            while True:
                if game.current_player == 'X':  # AI player
                    start_time = time.time()
                    col = game.best_move(depth)
                    move_time = time.time() - start_time
                    game_times.append(move_time)
                    game_moves.append(('AI', col))
                    game.make_move(col)
                else:  # Random player
                    valid_moves = game.get_valid_moves()
                    if valid_moves:
                        col = random.choice(valid_moves)
                        game_moves.append(('Random', col))
                        game.make_move(col)
                    else:
                        break
                
                moves += 1
                
                # Check if game is over
                if c4f.win(game.bitboard['X']):
                    results['ai_wins'] += 1
                    winner = 'AI'
                    break
                elif c4f.win(game.bitboard['O']):
                    results['random_wins'] += 1
                    winner = 'Random'
                    break
                elif not game.get_valid_moves():
                    results['draws'] += 1
                    winner = 'Draw'
                    break
            
            results['games'].append({
                'game_id': game_num + 1,
                'winner': winner,
                'moves': moves,
                'move_sequence': game_moves[:10],  # First 10 moves
                'ai_avg_time': sum(game_times) / len(game_times) if game_times else 0
            })
            
            results['move_times'].extend(game_times)
            results['game_lengths'].append(moves)
            
            if (game_num + 1) % 20 == 0:
                print(f"  Completed {game_num + 1}/{num_games} games")
        
        # Calculate summary statistics
        results['ai_win_rate'] = (results['ai_wins'] / num_games) * 100
        results['random_win_rate'] = (results['random_wins'] / num_games) * 100
        results['draw_rate'] = (results['draws'] / num_games) * 100
        results['avg_game_length'] = sum(results['game_lengths']) / len(results['game_lengths'])
        results['avg_ai_move_time'] = sum(results['move_times']) / len(results['move_times']) if results['move_times'] else 0
        results['total_games'] = num_games
        
        print(f"  AI win rate: {results['ai_win_rate']:.1f}%")
        print(f"  Random win rate: {results['random_win_rate']:.1f}%")
        print(f"  Draw rate: {results['draw_rate']:.1f}%")
        
        return results
    
    def run_comprehensive_simulation(self):
        """Run all Connect4 simulations and collect comprehensive data"""
        print("=" * 60)
        print("COMPREHENSIVE CONNECT4 SIMULATION")
        print("=" * 60)
        
        start_time = time.time()
        
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'game': 'Connect4',
            'simulation_results': {}
        }
        
        # 1. Win rates vs random at different depths
        print("\n1. WIN RATES VS RANDOM AT DIFFERENT DEPTHS")
        print("-" * 50)
        depth_analysis = self.simulate_ai_vs_random_depth_analysis([2, 4, 6, 8, 10], 75)
        self.results['simulation_results']['depth_vs_random'] = depth_analysis
        
        # 2. AI vs AI performance comparisons
        print("\n2. AI VS AI PERFORMANCE COMPARISONS")
        print("-" * 50)
        ai_comparisons = self.simulate_ai_vs_ai_comparison([(8, 6), (8, 4), (6, 4), (10, 6)], 40)
        self.results['simulation_results']['ai_vs_ai_comparisons'] = ai_comparisons
        
        # 3. Opening move preferences
        print("\n3. OPENING MOVE PREFERENCES")
        print("-" * 50)
        opening_analysis = self.analyze_opening_move_preferences(8, 100)
        self.results['simulation_results']['opening_preferences'] = opening_analysis
        
        # Print opening move summary
        x_opening = opening_analysis['X']
        most_common_opening = max(x_opening.items(), key=lambda x: x[1]['percentage'])
        print(f"  Most common opening move: Column {most_common_opening[0]} ({most_common_opening[1]['percentage']:.1f}%)")
        
        # 4. Computation time scaling
        print("\n4. COMPUTATION TIME SCALING")
        print("-" * 50)
        timing_analysis = self.test_computation_time_scaling([2, 4, 6, 8, 10, 12], 15)
        self.results['simulation_results']['timing_analysis'] = timing_analysis
        
        # 5. Detailed win rate analysis
        print("\n5. DETAILED WIN RATE ANALYSIS")
        print("-" * 50)
        detailed_analysis = self.simulate_win_rate_vs_random(120, 8)
        self.results['simulation_results']['detailed_win_analysis'] = detailed_analysis
        
        # 6. Performance metrics
        total_time = time.time() - start_time
        total_games = (5*75 + 4*40 + 100 + 120)  # Sum of all games
        
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
        filename = os.path.join(output_dir, f'connect4_comprehensive_results_{timestamp}.json')
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print("\n" + "=" * 60)
        print("CONNECT4 SIMULATION COMPLETE")
        print("=" * 60)
        print(f"Total games simulated: {total_games}")
        print(f"Total time: {total_time:.1f} seconds")
        print(f"Games per second: {total_games / total_time:.1f}")
        print(f"Results saved to: {filename}")
        
        return self.results, filename

def main():
    """Main function to run the comprehensive simulation"""
    simulation = Connect4ComprehensiveSimulation()
    results, filename = simulation.run_comprehensive_simulation()
    
    print(f"\nSimulation data saved to: {filename}")
    print("This data can now be used by visualization scripts.")

if __name__ == "__main__":
    main()