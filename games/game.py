import random
import time
import test as c4f

class ConnectFour:
    BOTTOM_MASK = [1 << (c * 7) for c in range(7)]
    BOARD_MASK = [((1 << 6) - 1) << (c * 7) for c in range(7)]
    TOP_MASK = [1 << (c * 7 + 6 - 1) for c in range(7)]

    def __init__(self):
        random.seed()
        self.bitboard = {'X': 0, 'O': 0}
        self.current_player = random.choice(['X', 'O'])

    def mask(self) -> int:
        return self.bitboard['X'] | self.bitboard['O']

    def can_play(self, col: int) -> bool:
        return (self.mask() & self.TOP_MASK[col]) == 0

    def get_valid_moves(self):
        return [c for c in range(7) if self.can_play(c)]

    def play_move(self, col: int, player: str):
        move = (self.mask() + self.BOTTOM_MASK[col]) & self.BOARD_MASK[col]
        self.bitboard[player] |= move

    def opponent_symbol(self) -> str:
        return 'O' if self.current_player == 'X' else 'X'

    def best_move(self, depth: int) -> int:
        cur = self.bitboard[self.current_player]
        opp = self.bitboard[self.opponent_symbol()]
        return c4f.find_best(cur, opp, depth)

    def make_move(self, col: int):
        self.play_move(col, self.current_player)
        self.current_player = self.opponent_symbol()

    def print_board(self):
        grid = [[' ' for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        for c in range(self.WIDTH):
            for r in range(self.HEIGHT):
                bit = 1 << (c * self.BITS_PER_COLUMN + r)
                if self.bitboard['X'] & bit:
                    grid[r][c] = 'X'
                elif self.bitboard['O'] & bit:
                    grid[r][c] = 'O'
        print('\n   ' + '   '.join(str(c) for c in range(self.WIDTH)))
        for r in range(self.HEIGHT - 1, -1, -1):
            print(f"{r}  " + ' | '.join(grid[r][c] for c in range(self.WIDTH)))
            if r > 0:
                print('   ' + '---+' * (self.WIDTH - 1) + '---')
        print()

def main():
    game  = ConnectFour()
    human = 'X'
    depth = 8

    print(f"starting player: {game.current_player}")
    game.print_board()

    while True:
        if game.current_player == human:
            valid = game.get_valid_moves()
            print(f"your turn ({human})")
            col = None
            while col not in valid:
                try:
                    col = int(input(f"choose column 0‑{game.WIDTH - 1}: "))
                except ValueError:
                    col = None
            game.make_move(col)
        else:
            print("ai thinking...")
            t0 = time.time()
            col = game.best_move(depth)
            print(f"ai plays column {col} ({time.time() - t0:.3f}s)")
            game.make_move(col)

        game.print_board()

        if c4f.win(game.bitboard['X']):
            print("X wins")
            break
        if c4f.win(game.bitboard['O']):
            print("O wins")
            break
        if not game.get_valid_moves():
            print("draw")
            break

if __name__ == "__main__":
    main()
