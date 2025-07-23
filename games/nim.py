import copy
import random
import time
import json
from datetime import datetime

class NimGame:
    def __init__(self, initial_piles=[3, 4, 5]):
        self.piles = initial_piles.copy()
        self.visited_nodes = 0  # For performance tracking
        self.move_history = []  # Track game moves
        
    def make_move(self, pile_idx, stones):
        """Validate and execute a move"""
        if 0 <= pile_idx < len(self.piles) and 1 <= stones <= self.piles[pile_idx]:
            move = (pile_idx, stones, self.piles[pile_idx])
            self.piles[pile_idx] -= stones
            self.move_history.append(move)
            return True
        return False
    
    def is_game_over(self):
        """Check if all piles are empty"""
        return all(pile == 0 for pile in self.piles)
    
    def generate_moves(self):
        """Generate all legal moves from current state"""
        moves = []
        for pile_idx, stones in enumerate(self.piles):
            for take in range(1, stones + 1):
                moves.append((pile_idx, take))
        return moves
    
    def copy(self):
        """Create a deep copy of the game state"""
        new_game = NimGame(self.piles)
        new_game.visited_nodes = self.visited_nodes
        new_game.move_history = self.move_history.copy()
        return new_game
    
    def display(self):
        """Print current game state"""
        print("\nCurrent piles:")
        for i, stones in enumerate(self.piles):
            print(f"Pile {i}: {'O ' * stones}({stones})")
        print(f"Nim-sum: {calculate_nim_sum(self.piles)}")

def calculate_nim_sum(piles):
    """Calculate the XOR of all pile sizes"""
    nim_sum = 0
    for pile in piles:
        nim_sum ^= pile
    return nim_sum

def optimal_nim_move(piles):
    """
    Find the optimal move using Nim-sum strategy
    Returns (pile_index, stones_to_take) or None if in losing position
    """
    nim_sum = calculate_nim_sum(piles)
    if nim_sum == 0:
        return None  # Losing position
    
    for i, pile in enumerate(piles):
        target = pile ^ nim_sum
        if target < pile:
            return (i, pile - target)
    return None

def minimax(game_state, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
    """Minimax algorithm with alpha-beta pruning and depth limiting"""
    game_state.visited_nodes += 1
    
    # Base case: terminal state
    if game_state.is_game_over():
        return 1 if not is_maximizing else -1  # Previous mover wins
    
    # Depth limit reached - use heuristic evaluation
    if depth == 0:
        nim_sum = calculate_nim_sum(game_state.piles)
        return 1 if nim_sum != 0 else -1
    
    if is_maximizing:
        max_eval = float('-inf')
        for move in game_state.generate_moves():
            new_state = game_state.copy()
            new_state.make_move(*move)
            eval = minimax(new_state, depth-1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in game_state.generate_moves():
            new_state = game_state.copy()
            new_state.make_move(*move)
            eval = minimax(new_state, depth-1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(game_state, depth=8, use_nim_sum=True):
    """
    Find the best move using Nim-sum strategy if possible,
    otherwise fall back to depth-limited minimax.
    """
    # First try mathematical optimal strategy if enabled
    if use_nim_sum:
        math_move = optimal_nim_move(game_state.piles)
        if math_move and math_move in game_state.generate_moves():
            return math_move, 1  # Only 1 node evaluated
        elif math_move is None:
            # We're in a losing position - all moves are equally bad
            # Return a random move since we can't win anyway
            import random
            moves = game_state.generate_moves()
            if moves:
                return random.choice(moves), 1
    
    # Use minimax with depth limiting
    best_move = None
    best_value = float('-inf')
    game_state.visited_nodes = 0
    
    for move in game_state.generate_moves():
        new_state = game_state.copy()
        new_state.make_move(*move)
        move_value = minimax(new_state, depth-1, is_maximizing=False)
        
        if move_value > best_value or (move_value == best_value and best_move is None):
            best_value = move_value
            best_move = move
    
    return best_move, game_state.visited_nodes

def random_move(game_state):
    """Select a random valid move"""
    moves = game_state.generate_moves()
    return random.choice(moves) if moves else None

def simulate_game(agent1_type="minimax", agent2_type="random", initial_piles=[3, 4, 5], 
                  depth=8, verbose=False):
    """
    Simulate a single game between two agents
    Returns: (winner, game_length, moves_history, nodes_evaluated)
    """
    game = NimGame(initial_piles)
    current_player = 1
    total_nodes = 0
    game_moves = []
    
    while not game.is_game_over():
        if verbose:
            game.display()
            print(f"\nPlayer {current_player}'s turn")
        
        # Determine move based on agent type
        if (current_player == 1 and agent1_type == "minimax") or \
           (current_player == 2 and agent2_type == "minimax"):
            best_move, nodes = find_best_move(game, depth)
            total_nodes += nodes
        elif (current_player == 1 and agent1_type == "nim_sum") or \
             (current_player == 2 and agent2_type == "nim_sum"):
            best_move, nodes = find_best_move(game, depth, use_nim_sum=True)
            total_nodes += nodes
        else:  # random player
            best_move = random_move(game)
            nodes = 1
            total_nodes += nodes
        
        if best_move is None:
            break
            
        pile_idx, stones = best_move
        game_moves.append((current_player, pile_idx, stones))
        
        if verbose:
            print(f"Player {current_player} takes {stones} stones from pile {pile_idx}")
        
        game.make_move(pile_idx, stones)
        current_player = 3 - current_player  # Switch player
    
    winner = 3 - current_player  # Previous player wins
    if verbose:
        game.display()
        print(f"\nPlayer {winner} wins!")
    
    return winner, len(game_moves), game_moves, total_nodes

def run_simulation_batch(num_games=100, agent1_type="minimax", agent2_type="random", 
                        initial_piles=[3, 4, 5], depth=8):
    """
    Run a batch of simulations and collect statistics
    """
    results = {
        'agent1_wins': 0,
        'agent2_wins': 0,
        'game_lengths': [],
        'total_nodes': 0,
        'game_details': []
    }
    
    print(f"Running {num_games} simulations: {agent1_type} vs {agent2_type}")
    print(f"Initial piles: {initial_piles}, Search depth: {depth}")
    
    start_time = time.time()
    
    for i in range(num_games):
        winner, length, moves, nodes = simulate_game(
            agent1_type, agent2_type, initial_piles, depth
        )
        
        if winner == 1:
            results['agent1_wins'] += 1
        else:
            results['agent2_wins'] += 1
        
        results['game_lengths'].append(length)
        results['total_nodes'] += nodes
        results['game_details'].append({
            'game_id': i+1,
            'winner': winner,
            'length': length,
            'moves': moves,
            'nodes_evaluated': nodes
        })
        
        if (i + 1) % 20 == 0:
            print(f"Completed {i + 1}/{num_games} games...")
    
    end_time = time.time()
    
    # Calculate statistics
    results['agent1_win_rate'] = (results['agent1_wins'] / num_games) * 100
    results['agent2_win_rate'] = (results['agent2_wins'] / num_games) * 100
    results['avg_game_length'] = sum(results['game_lengths']) / len(results['game_lengths'])
    results['avg_nodes_per_game'] = results['total_nodes'] / num_games
    results['total_time'] = end_time - start_time
    results['games_per_second'] = num_games / results['total_time']
    
    return results

def analyze_depth_performance(depths=[2, 4, 6, 8, 10], num_games=50, initial_piles=[3, 4, 5]):
    """Analyze performance across different search depths"""
    depth_results = {}
    
    for depth in depths:
        print(f"\nTesting depth {depth}...")
        results = run_simulation_batch(
            num_games=num_games,
            agent1_type="minimax",
            agent2_type="random",
            initial_piles=initial_piles,
            depth=depth
        )
        
        depth_results[depth] = {
            'win_rate': results['agent1_win_rate'],
            'avg_length': results['avg_game_length'],
            'avg_nodes': results['avg_nodes_per_game'],
            'avg_time_per_game': results['total_time'] / num_games
        }
    
    return depth_results

def save_simulation_results(results, filename=None):
    """Save simulation results to JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/text/nim_simulation_results_{timestamp}.json"
    
    # Ensure output directory exists
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {filename}")
    return filename

def ai_vs_ai_game(initial_piles=[3, 4, 5], depth=8):
    """Run an interactive game between two AI players"""
    print("Starting Nim Game with two AI players")
    print("The player who takes the last stone wins!\n")
    
    winner, length, moves, nodes = simulate_game(
        agent1_type="nim_sum",
        agent2_type="minimax",
        initial_piles=initial_piles,
        depth=depth,
        verbose=True
    )
    
    print(f"\nGame completed in {length} moves")
    print(f"Total nodes evaluated: {nodes}")
    return winner, length, moves, nodes

def comprehensive_nim_analysis():
    """Run comprehensive analysis of Nim game performance"""
    print("=" * 60)
    print("COMPREHENSIVE NIM GAME ANALYSIS")
    print("=" * 60)
    
    results = {}
    
    # 1. Basic performance analysis
    print("\n1. BASIC PERFORMANCE ANALYSIS")
    print("-" * 40)
    basic_results = run_simulation_batch(
        num_games=100,
        agent1_type="nim_sum",
        agent2_type="random",
        initial_piles=[3, 4, 5],
        depth=8
    )
    results['basic_performance'] = basic_results
    print(f"Nim-sum vs Random: {basic_results['agent1_win_rate']:.1f}% win rate")
    
    # 2. Depth analysis
    print("\n2. SEARCH DEPTH ANALYSIS")
    print("-" * 40)
    depth_results = analyze_depth_performance(
        depths=[2, 4, 6, 8, 10],
        num_games=50,
        initial_piles=[3, 4, 5]
    )
    results['depth_analysis'] = depth_results
    
    # 3. Different initial configurations
    print("\n3. INITIAL CONFIGURATION ANALYSIS")
    print("-" * 40)
    configurations = [
        [1, 2, 3],
        [3, 4, 5],
        [2, 4, 6],
        [1, 3, 5, 7]
    ]
    
    config_results = {}
    for config in configurations:
        print(f"Testing configuration {config}...")
        config_result = run_simulation_batch(
            num_games=50,
            agent1_type="nim_sum",
            agent2_type="random",
            initial_piles=config,
            depth=8
        )
        config_results[str(config)] = config_result
    
    results['configuration_analysis'] = config_results
    
    # 4. Agent comparison
    print("\n4. AGENT TYPE COMPARISON")
    print("-" * 40)
    agent_comparisons = {
        'nim_sum_vs_random': run_simulation_batch(100, "nim_sum", "random"),
        'minimax_vs_random': run_simulation_batch(100, "minimax", "random"),
        'nim_sum_vs_minimax': run_simulation_batch(100, "nim_sum", "minimax")
    }
    results['agent_comparison'] = agent_comparisons
    
    # Save comprehensive results
    filename = save_simulation_results(results, "output/text/nim_comprehensive_analysis.json")
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"Results saved to: {filename}")
    
    return results

if __name__ == "__main__":
    print("Nim Game Analysis")
    print("1. Run interactive AI vs AI game")
    print("2. Run comprehensive analysis")
    print("3. Run basic simulation")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        ai_vs_ai_game()
    elif choice == "2":
        comprehensive_nim_analysis()
    elif choice == "3":
        results = run_simulation_batch(100, "nim_sum", "random")
        save_simulation_results(results)
    else:
        print("Invalid choice. Running default comprehensive analysis...")
        comprehensive_nim_analysis()