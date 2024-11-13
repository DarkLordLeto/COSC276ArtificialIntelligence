import chess
import time

class IterativeDeepeningAI():
    def __init__(self, max_depth, time_limit=10):
        self.max_depth = max_depth
        self.time_limit = time_limit  # Time limit in seconds
        self.call = 0
        self.best_move = None
        self.start_time = None

    def choose_move(self, board):
        self.start_time = time.time()
        self.call = 0
        current_depth = 1

        while current_depth <= self.max_depth:
            if self.is_time_up():
                break

            try:
                value, move = self.alphaBeta(board, current_depth, float('-inf'), float('inf'), board.turn)
                # Only update best_move if we completed the full depth search
                if not self.is_time_up():
                    self.best_move = move
                    print(f"Depth {current_depth} completed - Best move: {move} with value {value}")
                current_depth += 1
            except TimeoutException:
                break

        print(f"Final recommendation - move {self.best_move}")
        print(f"Searched to depth: {current_depth - 1}")
        print(f"Number of positions evaluated: {self.call}")
        print(f"Time taken: {time.time() - self.start_time:.2f} seconds")
        
        return self.best_move

    def is_time_up(self):
        return time.time() - self.start_time >= self.time_limit

    def cutoffTest(self, board, depth):
        if self.is_time_up():
            raise TimeoutException()
        return depth == 0 or board.is_game_over() or not board.legal_moves
    
    def alphaBeta(self, board, depth, alpha, beta, isMaximizing):
        self.call += 1
        if self.cutoffTest(board, depth):
            return self.evaluate(board), None
        
        bestMove = None
        if isMaximizing:
            maxScore = float('-inf')
            for move in self.moveOrdering(board):
                board.push(move)
                score, _ = self.alphaBeta(board, depth-1, alpha, beta, False)
                board.pop()
                
                if score > maxScore:
                    maxScore = score
                    bestMove = move
                alpha = max(alpha, maxScore)
                if alpha >= beta:
                    break
            return maxScore, bestMove
            
        else:
            minScore = float('inf')
            for move in self.moveOrdering(board):
                board.push(move)
                score, _ = self.alphaBeta(board, depth-1, alpha, beta, True)
                board.pop()
                
                if score < minScore:
                    minScore = score
                    bestMove = move
                beta = min(beta, minScore)
                if beta <= alpha:
                    break
            return minScore, bestMove
        
    def evaluate(self, board):
        if board.is_checkmate():
            return float('inf') if board.turn else float('-inf')
            
        if board.is_stalemate() or board.is_insufficient_material():
            return 0.0
        
        score = 0
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 1000
        }
        
        for piece, value in piece_values.items():
            score += len(board.pieces(piece, chess.WHITE)) * value
            score -= len(board.pieces(piece, chess.BLACK)) * value
        return score
    
    def moveOrdering(self, board):
        capture_moves = []
        non_capture_moves = []
        for move in board.legal_moves:
            if board.is_capture(move):
                capture_moves.append(move)
            else:
                non_capture_moves.append(move)
        return capture_moves + non_capture_moves

class TimeoutException(Exception):
    pass