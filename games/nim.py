class NimGame:
    def __init__(self, initial_piles=[3, 4, 5]):
        self.piles = initial_piles.copy()
        self.visited_nodes = 0

    def make_move(self, pile_idx, stones):
        if 0 <= pile_idx < len(self.piles) and 1 <= stones <= self.piles[pile_idx]:
            self.piles[pile_idx] -= stones
            return True
        return False

    def is_game_over(self):
        return all(pile == 0 for pile in self.piles)

    def generate_moves(self):
        moves = []
        for pile_idx, stones in enumerate(self.piles):
            for take in range(1, stones + 1):
                moves.append((pile_idx, take))
        return moves

    def evaluate(self):
        # 游戏结束时，当前玩家获胜（因为他拿走了最后一个石子）
        return 1 if self.is_game_over() else 0

    def copy(self):
        new_game = NimGame(self.piles)
        new_game.visited_nodes = self.visited_nodes
        return new_game

    def display(self):
        print("\nCurrent piles:")
        for i, stones in enumerate(self.piles):
            print(f"Pile {i}: {'O ' * stones}")


def minimax(game_state, depth, is_maximizing_player, alpha=float('-inf'), beta=float('inf')):
    game_state.visited_nodes += 1
    
    if game_state.is_game_over():
        # 如果是最大化玩家的回合时游戏结束，说明最小化玩家拿走了最后一个石子
        # 所以最大化玩家输了（返回-1），最小化玩家赢了（返回1）
        return 1 if not is_maximizing_player else -1
    
    if depth == 0:
        # 非终端节点，使用Nim-sum评估
        nim_sum = 0
        for pile in game_state.piles:
            nim_sum ^= pile
        return 1 if nim_sum != 0 else -1
    
    if is_maximizing_player:
        max_eval = float('-inf')
        for move in game_state.generate_moves():
            new_state = game_state.copy()
            new_state.make_move(*move)
            eval = minimax(new_state, depth - 1, False, alpha, beta)
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
            eval = minimax(new_state, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def find_best_move(game_state, depth=10):
    best_move = None
    best_value = float('-inf')
    
    for move in game_state.generate_moves():
        new_state = game_state.copy()
        new_state.make_move(*move)
        move_value = minimax(new_state, depth - 1, False)
        
        if move_value > best_value or (move_value == best_value and best_move is None):
            best_value = move_value
            best_move = move
    
    return best_move, game_state.visited_nodes


def bot_vs_bot_game(initial_piles=[3, 4, 5]):
    game = NimGame(initial_piles)
    current_player = 1
    
    while not game.is_game_over():
        game.display()
        print(f"\nBot Player {current_player}'s turn")
        
        game.visited_nodes = 0
        best_move, nodes_evaluated = find_best_move(game)
        
        if best_move is None:
            # 如果没有合法移动，当前玩家输
            print("No valid moves left!")
            break
            
        pile_idx, stones = best_move
        print(f"Bot Player {current_player} takes {stones} stones from pile {pile_idx}")
        print(f"Nodes evaluated: {nodes_evaluated}")
        
        game.make_move(pile_idx, stones)
        current_player = 3 - current_player
    
    game.display()
    # Current player is the next player to move, but since game is over, previous player wins
    print(f"\nBot Player {3 - current_player} wins by taking the last stone!")


if __name__ == "__main__":
    print("Starting Nim Game with two bot players using Minimax algorithm")
print("The player who takes the last stone wins!")
bot_vs_bot_game()