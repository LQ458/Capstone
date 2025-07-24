class HalvingGame:
    def __init__(self, initial_number):
        self.initial_number = initial_number
    
    def get_moves(self, current_number):
        #Return all possible legal moves for current number (halve or subtract one)
        moves = []
        if current_number > 1:
            moves.append(current_number - 1)
            moves.append(current_number // 2)
        return moves
    
    def minimax(self, current_number, is_maximizing, depth=0, alpha=float('-inf'), beta=float('inf')):
        # Minimax algorithm  with alpha-beta pruning
        
        # Base case: game over
        if current_number==1:
            return (1 if not is_maximizing else -1, None)  # Previous player wins
        
        if is_maximizing:
            best_value = float('-inf')
            best_move = None
            for move in self.get_moves(current_number):
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
            for move in self.get_moves(current_number):
                value, _ = self.minimax(move, True, depth+1, alpha, beta)
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break  # Alpha pruning
            return (best_value, best_move)
    
    def play_game(self):
        #Simulate two agent players using Minimax algorithm
        current_number = self.initial_number
        current_player = 1
        print(f"Game starts with initial number: {current_number}")

        while current_number>1:
            is_maximizing = (current_player == 1)
            _, move = self.minimax(current_number, is_maximizing)
            
            operation = "-1" if move == current_number - 1 else "/2"
            print(f"Player {current_player} changes {current_number}{operation} => {move}")
            current_number = move
            
            # Switch players
            current_player = 2 if current_player == 1 else 1
        
        winner = 2 if current_player == 1 else 1
        print(f"Game over! Player {winner} wins!")

if __name__ == "__main__":
    initial_number = int(input("Please input an initial number greater than 1: "))
    game = HalvingGame(initial_number)
    game.play_game()