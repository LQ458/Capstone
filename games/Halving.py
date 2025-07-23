class HalvingGame:
    def __init__(self, initial_number):
        self.initial_number = initial_number
    
    def get_possible_moves(self, current_number):
        """返回当前数字所有可能的合法移动（减半或减一）"""
        moves = []
        if current_number > 1:  # 只有大于1时才能操作
            moves.append(current_number - 1)      # 减一
            moves.append(current_number // 2)      # 减半（向下取整）
        return moves
    
    def is_terminal(self, current_number):
        """检查游戏是否结束（当前数字为1）"""
        return current_number == 1
    
    def minimax(self, current_number, is_maximizing, depth=0, alpha=float('-inf'), beta=float('inf')):
        """
        Minimax算法实现，带有alpha-beta剪枝
        返回：(最佳移动的评估值, 最佳移动)
        """
        
        # 基础情况：游戏结束
        if self.is_terminal(current_number):
            return (1 if not is_maximizing else -1, None)  # 上一个玩家获胜
        
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
                    break  # beta剪枝
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
                    break  # alpha剪枝
            return (best_value, best_move)
    
    def play_game(self):
        """模拟两个AI玩家使用Minimax算法进行游戏"""
        current_number = self.initial_number
        current_player = 1  # 玩家1是Maximizing玩家
        
        print(f"游戏开始，初始数字: {current_number}")
        
        while not self.is_terminal(current_number):
            is_maximizing = (current_player == 1)
            _, move = self.minimax(current_number, is_maximizing)
            
            operation = "-1" if move == current_number - 1 else "/2"
            print(f"玩家{current_player} 将数字 {current_number} {operation} => {move}")
            current_number = move
            
            # 切换玩家
            current_player = 2 if current_player == 1 else 1
        
        winner = 2 if current_player == 1 else 1
        print(f"游戏结束！玩家 {winner} 获胜！")


initial_number = 2  # 默认初始数字

game = HalvingGame(initial_number)
game.play_game()