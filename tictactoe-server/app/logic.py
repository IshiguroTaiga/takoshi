class TicTacToe:
    def __init__(self, board_str="         "):
        self.board = list(board_str)

    def make_move(self, index, char):
        if self.board[index] == " ":
            self.board[index] = char
            return True
        return False

    def check_winner(self):
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in lines:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]
        if " " not in self.board: return "Draw"
        return None

    def get_ai_move(self):
        best_score = -float('inf')
        move = -1
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(self.board, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def minimax(self, board, is_max):
        res = self.check_winner_static(board)
        if res == "O": return 1
        if res == "X": return -1
        if res == "Draw": return 0
        
        scores = []
        for i in range(9):
            if board[i] == " ":
                board[i] = "O" if is_max else "X"
                scores.append(self.minimax(board, not is_max))
                board[i] = " "
        return max(scores) if is_max else min(scores)

    @staticmethod
    def check_winner_static(board):
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in lines:
            if board[a] == board[b] == board[c] != " ": return board[a]
        if " " not in board: return "Draw"
        return None