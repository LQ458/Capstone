import time

# Define constants
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
DRAW = 3

# Define board display characters
BOARD_CHARS = {
    EMPTY: ' ',
    PLAYER_X: 'X',
    PLAYER_O: 'O'
}

class TicTacToe:
    """
    Tic Tac Toe game implementation with optimized Minimax AI algorithm
    """
    
    def __init__(self):
        # Initialize empty 3x3 board using nested lists
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = PLAYER_X  # X goes first
        self.game_over = False
        self.winner = None
        self.move_count = 0  # Track number of moves
        
    def print_board(self):
        """Display the current board state with coordinates"""
        print("  0 1 2")
        for i in range(3):
            row = [BOARD_CHARS[self.board[i][j]] for j in range(3)]
            print(f"{i} {'|'.join(row)}")
            if i < 2:
                print("  -----")
        print()
    
    def is_valid_move(self, row, col):
        """Check if a move is valid (within bounds and position is empty)"""
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == EMPTY
    
    def make_move(self, row, col):
        """Make a move on the board and update game state"""
        if self.game_over or not self.is_valid_move(row, col):
            return False
        
        self.board[row][col] = self.current_player
        self.move_count += 1
        self.check_game_over()
        
        if not self.game_over:
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
        
        return True
    
    def get_available_moves(self):
        """Get all available (empty) positions on the board"""
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == EMPTY]
    
    def check_game_over(self):
        """Check if the game is over and determine winner"""
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != EMPTY:
                self.game_over = True
                self.winner = self.board[i][0]
                return
        
        # Check columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != EMPTY:
                self.game_over = True
                self.winner = self.board[0][j]
                return
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != EMPTY:
            self.game_over = True
            self.winner = self.board[0][0]
            return
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != EMPTY:
            self.game_over = True
            self.winner = self.board[0][2]
            return
        
        # Check for draw
        if all(self.board[i][j] != EMPTY for i in range(3) for j in range(3)):
            self.game_over = True
            self.winner = DRAW
    
    def is_first_move(self):
        """Check if this is the first move of the game"""
        return self.move_count == 0
    
    def evaluate_board(self):
        """Evaluate the board state for minimax algorithm
        Returns: 10 for X win, -10 for O win, 0 for draw or ongoing game
        """
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != EMPTY:
                return 10 if self.board[i][0] == PLAYER_X else -10
        
        # Check columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != EMPTY:
                return 10 if self.board[0][j] == PLAYER_X else -10
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != EMPTY:
            return 10 if self.board[0][0] == PLAYER_X else -10
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != EMPTY:
            return 10 if self.board[0][2] == PLAYER_X else -10
        
        # Draw or ongoing game
        return 0
    
    def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        """
        Minimax algorithm with Alpha-Beta pruning and depth consideration
        Args:
            depth: Current depth in the search tree
            is_maximizing: True if current player is maximizing (X), False if minimizing (O)
            alpha: Best score for maximizing player
            beta: Best score for minimizing player
        Returns:
            Best score for the current player
        """
        score = self.evaluate_board()
        
        # Terminal state evaluation with depth consideration
        if score == 10:
            return score - depth  # Prefer faster wins
        if score == -10:
            return score + depth  # Prefer slower losses
        if len(self.get_available_moves()) == 0:
            return 0
        
        if is_maximizing:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = PLAYER_X
                        best = max(best, self.minimax(depth + 1, False, alpha, beta))
                        self.board[i][j] = EMPTY
                        # Alpha-Beta pruning
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = PLAYER_O
                        best = min(best, self.minimax(depth + 1, True, alpha, beta))
                        self.board[i][j] = EMPTY
                        # Alpha-Beta pruning
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best
    
    def find_best_move(self):
        """Find the best move for the current player using minimax algorithm"""
        # Special case: if it's the first move and center is available, choose center
        if self.is_first_move() and self.board[1][1] == EMPTY:
            return (1, 1)
        
        best_val = float('-inf') if self.current_player == PLAYER_X else float('inf')
        best_move = (-1, -1)
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = self.current_player
                    move_val = self.minimax(0, self.current_player == PLAYER_O)
                    self.board[i][j] = EMPTY
                    
                    if self.current_player == PLAYER_X:
                        if move_val > best_val or (move_val == best_val and best_move == (-1, -1)):
                            best_move = (i, j)
                            best_val = move_val
                    else:
                        if move_val < best_val or (move_val == best_val and best_move == (-1, -1)):
                            best_move = (i, j)
                            best_val = move_val
        
        return best_move
    
    def get_human_move(self):
        """Get move from human player with input validation"""
        while True:
            try:
                print(f"Your turn ({BOARD_CHARS[self.current_player]}). Enter row and column (0-2):")
                row = int(input("Row: "))
                col = int(input("Column: "))
                
                if self.is_valid_move(row, col):
                    return row, col
                else:
                    print("Invalid move! Position is either out of bounds or already occupied.")
            except ValueError:
                print("Invalid input! Please enter numbers between 0 and 2.")
    
    def play_game(self):
        """Main game loop for human vs AI"""
        print("Welcome to Tic Tac Toe!")
        print("You are X, AI is O")
        print("Enter row and column numbers (0-2) to make your move")
        
        while not self.game_over:
            self.print_board()
            
            if self.current_player == PLAYER_X:
                # Human's turn
                row, col = self.get_human_move()
                self.make_move(row, col)
                print(f"You placed {BOARD_CHARS[PLAYER_X]} at ({row}, {col})")
            else:
                # AI's turn
                print("AI is thinking...")
                row, col = self.find_best_move()
                self.make_move(row, col)
                print(f"AI placed {BOARD_CHARS[PLAYER_O]} at ({row}, {col})")
        
        # Game over
        self.print_board()
        if self.winner == DRAW:
            print("It's a draw!")
        else:
            winner_char = BOARD_CHARS[self.winner]
            if self.winner == PLAYER_X:
                print("Congratulations! You win!")
            else:
                print("AI wins! Better luck next time!")
    
    def play_ai_vs_ai(self):
        """AI vs AI simulation for testing"""
        print("AI vs AI simulation")
        print("Both players use Minimax algorithm")
        print(f"{BOARD_CHARS[PLAYER_X]} player goes first\n")
        
        while not self.game_over:
            self.print_board()
            
            if self.current_player == PLAYER_X:
                print(f"{BOARD_CHARS[PLAYER_X]} player thinking...")
            else:
                print(f"{BOARD_CHARS[PLAYER_O]} player thinking...")
            
            # Add small delay to make the game observable
            time.sleep(0.5)
            
            row, col = self.find_best_move()
            self.make_move(row, col)
        
        self.print_board()
        
        if self.winner == DRAW:
            print("Game over, it's a draw!")
        else:
            winner_char = BOARD_CHARS[self.winner]
            print(f"Game over, {winner_char} player wins!")

def main():
    """Main function to start the game"""
    game = TicTacToe()
    
    # Choose game mode
    print("Choose game mode:")
    print("1. Human vs AI")
    print("2. AI vs AI")
    
    while True:
        try:
            choice = int(input("Enter your choice (1 or 2): "))
            if choice == 1:
                game.play_game()
                break
            elif choice == 2:
                game.play_ai_vs_ai()
                break
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()