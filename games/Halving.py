class HalvingGame:
    def __init__(self, initial_number):
        self.initial_number = initial_number
    
    def get_possible_moves(self, current_number):
        """Return all possible legal moves for current number (halve or subtract one)"""
        moves = []
        if current_number > 1:  # Only operate when greater than 1
            moves.append(current_number - 1)      # Subtract one
            moves.append(current_number // 2)      # Halve (floor division)
        return moves
    
    def is_game_over(self, current_number):
        """Check if game is over (current number is 1)"""
        return current_number == 1
    
    def minimax(self, current_number, is_maximizing, depth=0, alpha=float('-inf'), beta=float('inf')):
        """
        Minimax algorithm implementation with alpha-beta pruning
        Returns: (best move evaluation value, best move)
        """
        
        # Base case: game over
        if self.is_game_over(current_number):
            return (1 if not is_maximizing else -1, None)  # Previous player wins
        
        if is_maximizing:
            best_value = float('-inf')
            best_move = None
            for move in self.get_possible_moves(current_number):
                value, _ = self.minimax(move, False, depth+1, alpha, beta)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break  # Beta pruning
            return (best_value, best_move)
        else:
            best_value = float('inf')
            best_move = None
            for move in self.get_possible_moves(current_number):
                value, _ = self.minimax(move, True, depth+1, alpha, beta)
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break  # Alpha pruning
            return (best_value, best_move)
    
    def play_game(self):
        """Simulate two agent players using Minimax algorithm"""
        current_number = self.initial_number
        current_player = 1  # Player 1 is the maximizing player
        
        print(f"Game starts with initial number: {current_number}")
        
        while not self.is_game_over(current_number):
            is_maximizing = (current_player == 1)
            _, move = self.minimax(current_number, is_maximizing)
            
            operation = "-1" if move == current_number - 1 else "/2"
            print(f"Player {current_player} changes {current_number} {operation} => {move}")
            current_number = move
            
            # Switch players
            current_player = 2 if current_player == 1 else 1
        
        winner = 2 if current_player == 1 else 1
        print(f"Game over! Player {winner} wins!")


initial_number = 20  # Default initial number

game = HalvingGame(initial_number)
game.play_game()