#!/usr/bin/env python3
"""
Comprehensive Halving Game Simulation Script
Runs real simulations to collect data for visualization
"""

import sys
import os
import json
import time
import random
from datetime import datetime

# Import the Halving game
sys.path.append(os.path.join(os.path.dirname(__file__), '../../games'))
from Halving import HalvingGame

class HalvingComprehensiveSimulation:
    """Comprehensive simulation class for Halving Game"""
    
    def __init__(self):
        self.results = {}
    
    def simulate_with_different_initial_numbers(self, initial_numbers=[10, 15, 20, 25, 30, 50, 75, 100], games_per_number=50):
        """Test win rates with different initial numbers"""
        print(f"Running simulations with different initial numbers...")
        
        number_results = {}
        
        for initial_num in initial_numbers:
            print(f"  Testing initial number {initial_num}...")
            
            player1_wins = 0
            player2_wins = 0
            game_lengths = []
            halving_moves = 0
            subtraction_moves = 0
            computation_times = []
            
            for game_num in range(games_per_number):
                game = HalvingGame(initial_num)
                current_number = initial_num
                current_player = 1
                moves = 0
                game_start_time = time.time()
                
                while current_number > 1:
                    is_maximizing = (current_player == 1)
                    
                    start_time = time.time()
                    _, move = game.minimax(current_number, is_maximizing)
                    move_time = time.time() - start_time
                    computation_times.append(move_time)
                    
                    # Track strategy preferences
                    if move == current_number // 2:
                        halving_moves += 1
                    else:  # move == current_number - 1
                        subtraction_moves += 1
                    
                    current_number = move
                    current_player = 2 if current_player == 1 else 1
                    moves += 1
                
                game_time = time.time() - game_start_time
                
                # Determine winner
                winner = 2 if current_player == 1 else 1
                if winner == 1:
                    player1_wins += 1
                else:
                    player2_wins += 1
                
                game_lengths.append(moves)
            
            number_results[initial_num] = {
                'initial_number': initial_num,
                'player1_wins': player1_wins,
                'player2_wins': player2_wins,
                'player1_win_rate': (player1_wins / games_per_number) * 100,
                'player2_win_rate': (player2_wins / games_per_number) * 100,
                'avg_game_length': sum(game_lengths) / len(game_lengths),
                'total_moves': sum(game_lengths),
                'halving_moves': halving_moves,
                'subtraction_moves': subtraction_moves,
                'halving_percentage': (halving_moves / (halving_moves + subtraction_moves)) * 100 if (halving_moves + subtraction_moves) > 0 else 0,
                'avg_computation_time': sum(computation_times) / len(computation_times) if computation_times else 0,
                'total_games': games_per_number
            }
            
            result = number_results[initial_num]
            print(f"    Player 1: {result['player1_win_rate']:.1f}% win rate")
            print(f"    Avg length: {result['avg_game_length']:.1f} moves")
            print(f"    Halving preference: {result['halving_percentage']:.1f}%")
        
        return number_results
    
    def analyze_strategy_preferences(self, initial_numbers=[10, 20, 30, 50, 100], games_per_number=30):
        """Analyze detailed strategy preferences (halving vs subtraction)"""
        print(f"Analyzing strategy preferences...")
        
        strategy_analysis = {}
        
        for initial_num in initial_numbers:
            print(f"  Analyzing initial number {initial_num}...")
            
            move_patterns = []
            decision_points = []
            
            for game_num in range(games_per_number):
                game = HalvingGame(initial_num)
                current_number = initial_num
                current_player = 1
                game_pattern = []
                
                while current_number > 1:
                    is_maximizing = (current_player == 1)
                    possible_moves = game.get_moves(current_number)
                    
                    if len(possible_moves) > 1:  # Decision point
                        _, optimal_move = game.minimax(current_number, is_maximizing)
                        
                        # Analyze what happens with each choice
                        move_analysis = {}
                        for possible_move in possible_moves:
                            # Simulate opponent's response
                            temp_game = HalvingGame(initial_num)
                            _, opponent_response = temp_game.minimax(possible_move, not is_maximizing)
                            
                            operation = "halve" if possible_move == current_number // 2 else "subtract"
                            move_analysis[possible_move] = {
                                'operation': operation,
                                'opponent_response': opponent_response,
                                'chosen': (possible_move == optimal_move)
                            }
                        
                        decision_points.append({
                            'number': current_number,
                            'player': current_player,
                            'analysis': move_analysis,
                            'optimal_choice': optimal_move
                        })
                    
                    _, move = game.minimax(current_number, is_maximizing)
                    operation = "halve" if move == current_number // 2 else "subtract"
                    
                    game_pattern.append({
                        'from': current_number,
                        'to': move,
                        'operation': operation,
                        'player': current_player
                    })
                    
                    current_number = move
                    current_player = 2 if current_player == 1 else 1
                
                move_patterns.append(game_pattern)
            
            # Analyze patterns
            total_halving = sum(1 for pattern in move_patterns for move in pattern if move['operation'] == 'halve')
            total_subtracting = sum(1 for pattern in move_patterns for move in pattern if move['operation'] == 'subtract')
            total_moves = total_halving + total_subtracting
            
            strategy_analysis[initial_num] = {
                'total_decision_points': len(decision_points),
                'total_halving_moves': total_halving,
                'total_subtracting_moves': total_subtracting,
                'halving_percentage': (total_halving / total_moves) * 100 if total_moves > 0 else 0,
                'subtracting_percentage': (total_subtracting / total_moves) * 100 if total_moves > 0 else 0,
                'decision_points_sample': decision_points[:5],  # First 5 for analysis
                'move_patterns_sample': move_patterns[:3]  # First 3 games
            }
            
            result = strategy_analysis[initial_num]
            print(f"    Decision points: {result['total_decision_points']}")
            print(f"    Halving preference: {result['halving_percentage']:.1f}%")
        
        return strategy_analysis
    
    def test_performance_scaling(self, numbers=list(range(10, 101, 10)), trials_per_number=10):
        """Test how performance scales with initial number size"""
        print(f"Testing performance scaling with number size...")
        
        scaling_results = {}
        
        for num in numbers:
            print(f"  Testing number {num}...")
            
            computation_times = []
            game_lengths = []
            
            for trial in range(trials_per_number):
                game = HalvingGame(num)
                current_number = num
                current_player = 1
                moves = 0
                total_computation_time = 0
                
                while current_number > 1:
                    is_maximizing = (current_player == 1)
                    
                    start_time = time.time()
                    _, move = game.minimax(current_number, is_maximizing)
                    computation_time = time.time() - start_time
                    total_computation_time += computation_time
                    
                    current_number = move
                    current_player = 2 if current_player == 1 else 1
                    moves += 1
                
                computation_times.append(total_computation_time)
                game_lengths.append(moves)
            
            scaling_results[num] = {
                'initial_number': num,
                'avg_total_computation_time': sum(computation_times) / len(computation_times),
                'avg_game_length': sum(game_lengths) / len(game_lengths),
                'avg_time_per_move': (sum(computation_times) / len(computation_times)) / (sum(game_lengths) / len(game_lengths)) if game_lengths else 0,
                'trials': trials_per_number
            }
            
            result = scaling_results[num]
            print(f"    Avg computation time: {result['avg_total_computation_time']:.4f}s")
            print(f"    Avg game length: {result['avg_game_length']:.1f} moves")
        
        return scaling_results
    
    def simulate_minimax_vs_random(self, initial_numbers=[15, 25, 50, 75], games_per_number=50):
        """Compare minimax strategy vs random strategy"""
        print(f"Running Minimax vs Random simulations...")
        
        comparison_results = {}
        
        for initial_num in initial_numbers:
            print(f"  Testing initial number {initial_num}...")
            
            minimax_wins = 0
            random_wins = 0
            game_lengths = []
            
            for game_num in range(games_per_number):
                game = HalvingGame(initial_num)
                current_number = initial_num
                current_player = 1  # Minimax player
                moves = 0
                
                while current_number > 1:
                    if current_player == 1:  # Minimax player
                        _, move = game.minimax(current_number, True)
                    else:  # Random player
                        possible_moves = game.get_moves(current_number)
                        move = random.choice(possible_moves) if possible_moves else current_number - 1
                    
                    current_number = move
                    current_player = 2 if current_player == 1 else 1
                    moves += 1
                
                game_lengths.append(moves)
                
                # Determine winner
                winner = 2 if current_player == 1 else 1
                if winner == 1:  # Minimax player wins
                    minimax_wins += 1
                else:  # Random player wins
                    random_wins += 1
            
            comparison_results[initial_num] = {
                'initial_number': initial_num,
                'minimax_wins': minimax_wins,
                'random_wins': random_wins,
                'minimax_win_rate': (minimax_wins / games_per_number) * 100,
                'random_win_rate': (random_wins / games_per_number) * 100,
                'avg_game_length': sum(game_lengths) / len(game_lengths),
                'total_games': games_per_number
            }
            
            result = comparison_results[initial_num]
            print(f"    Minimax win rate: {result['minimax_win_rate']:.1f}%")
            print(f"    Random win rate: {result['random_win_rate']:.1f}%")
        
        return comparison_results
    
    def analyze_optimal_first_moves(self, initial_numbers=list(range(5, 51, 5))):
        """Analyze optimal first moves for different starting numbers"""
        print(f"Analyzing optimal first moves...")
        
        first_move_analysis = {}
        
        for initial_num in initial_numbers:
            game = HalvingGame(initial_num)
            
            # Get optimal first move
            _, optimal_move = game.minimax(initial_num, True)
            optimal_operation = "halve" if optimal_move == initial_num // 2 else "subtract"
            
            # Analyze consequences of each possible first move
            possible_moves = game.get_moves(initial_num)
            move_consequences = {}
            
            for move in possible_moves:
                operation = "halve" if move == initial_num // 2 else "subtract"
                
                # Simulate opponent's best response
                _, opponent_move = game.minimax(move, False)
                
                # Evaluate the position after opponent's response
                evaluation, _ = game.minimax(opponent_move, True)
                
                move_consequences[move] = {
                    'operation': operation,
                    'opponent_response': opponent_move,
                    'evaluation': evaluation,
                    'is_optimal': (move == optimal_move)
                }
            
            first_move_analysis[initial_num] = {
                'initial_number': initial_num,
                'optimal_move': optimal_move,
                'optimal_operation': optimal_operation,
                'move_consequences': move_consequences,
                'halve_option': initial_num // 2,
                'subtract_option': initial_num - 1,
                'prefers_halving': (optimal_operation == "halve")
            }
            
            print(f"  Number {initial_num}: Optimal move is {optimal_operation} ({optimal_move})")
        
        return first_move_analysis
    
    def run_comprehensive_simulation(self):
        """Run all Halving Game simulations and collect comprehensive data"""
        print("=" * 60)
        print("COMPREHENSIVE HALVING GAME SIMULATION")
        print("=" * 60)
        
        start_time = time.time()
        
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'game': 'Halving Game',
            'simulation_results': {}
        }
        
        # 1. Win rates with different initial numbers
        print("\n1. WIN RATES WITH DIFFERENT INITIAL NUMBERS")
        print("-" * 50)
        number_analysis = self.simulate_with_different_initial_numbers([10, 15, 20, 25, 30, 40, 50, 75, 100], 40)
        self.results['simulation_results']['number_analysis'] = number_analysis
        
        # 2. Strategy preferences analysis
        print("\n2. STRATEGY PREFERENCES ANALYSIS")
        print("-" * 50)
        strategy_analysis = self.analyze_strategy_preferences([10, 20, 30, 50, 100], 25)
        self.results['simulation_results']['strategy_analysis'] = strategy_analysis
        
        # 3. Performance scaling
        print("\n3. PERFORMANCE SCALING ANALYSIS")
        print("-" * 50)
        scaling_analysis = self.test_performance_scaling(list(range(10, 101, 15)), 8)
        self.results['simulation_results']['scaling_analysis'] = scaling_analysis
        
        # 4. Minimax vs Random comparison
        print("\n4. MINIMAX VS RANDOM STRATEGY")
        print("-" * 50)
        comparison_analysis = self.simulate_minimax_vs_random([15, 25, 35, 50, 75], 40)
        self.results['simulation_results']['minimax_vs_random'] = comparison_analysis
        
        # 5. Optimal first moves analysis
        print("\n5. OPTIMAL FIRST MOVES ANALYSIS")
        print("-" * 50)
        first_move_analysis = self.analyze_optimal_first_moves(list(range(5, 51, 5)))
        self.results['simulation_results']['first_move_analysis'] = first_move_analysis
        
        # Calculate overall statistics
        total_halving_preference = 0
        total_numbers_tested = len(number_analysis)
        
        for result in number_analysis.values():
            total_halving_preference += result['halving_percentage']
        
        avg_halving_preference = total_halving_preference / total_numbers_tested if total_numbers_tested > 0 else 0
        
        print(f"\nOverall halving preference: {avg_halving_preference:.1f}%")
        
        # 6. Performance metrics
        total_time = time.time() - start_time
        total_games = (9*40 + 5*25 + 7*8 + 5*40)  # Sum of all games
        
        self.results['simulation_results']['performance_metrics'] = {
            'total_simulation_time': total_time,
            'total_games_simulated': total_games,
            'games_per_second': total_games / total_time,
            'avg_time_per_game': total_time / total_games,
            'avg_halving_preference': avg_halving_preference
        }
        
        # Save results to JSON
        output_dir = '../../output/text'
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f'halving_comprehensive_results_{timestamp}.json')
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print("\n" + "=" * 60)
        print("HALVING GAME SIMULATION COMPLETE")
        print("=" * 60)
        print(f"Total games simulated: {total_games}")
        print(f"Total time: {total_time:.1f} seconds")
        print(f"Games per second: {total_games / total_time:.1f}")
        print(f"Average halving preference: {avg_halving_preference:.1f}%")
        print(f"Results saved to: {filename}")
        
        return self.results, filename

def main():
    """Main function to run the comprehensive simulation"""
    simulation = HalvingComprehensiveSimulation()
    results, filename = simulation.run_comprehensive_simulation()
    
    print(f"\nSimulation data saved to: {filename}")
    print("This data can now be used by visualization scripts.")

if __name__ == "__main__":
    main()