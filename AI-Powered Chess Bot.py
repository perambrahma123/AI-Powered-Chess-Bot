import chess
import chess.engine
import chess.polyglot

class ChessAI:
    def __init__(self, depth=3):
        self.depth = depth

    def evaluate_board(self, board):
        """Simple evaluation function based on material count."""
        piece_values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, 
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 1000
        }
        eval_score = 0

        for piece_type in piece_values:
            eval_score += (
                len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type] -
                len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
            )
        return eval_score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with Alpha-Beta pruning."""
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        legal_moves = list(board.legal_moves)

        if maximizing_player:
            max_eval = -float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, board):
        """Finds the best move using Minimax with Alpha-Beta pruning."""
        best_move = None
        best_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for move in board.legal_moves:
            board.push(move)
            board_value = self.minimax(board, self.depth - 1, alpha, beta, False)
            board.pop()

            if board_value > best_value:
                best_value = board_value
                best_move = move

        return best_move

def play_chess():
    board = chess.Board()
    ai = ChessAI(depth=3)

    while not board.is_game_over():
        print(board)

        if board.turn == chess.WHITE:
            move = input("Your move (e.g., e2e4): ")
            try:
                board.push_uci(move)
            except ValueError:
                print("Invalid move. Try again.")
                continue
        else:
            print("AI is thinking...")
            ai_move = ai.find_best_move(board)
            print(f"AI moves: {ai_move}")
            board.push(ai_move)

    print("Game Over!")
    print(f"Result: {board.result()}")

if __name__ == "__main__":
    play_chess()
