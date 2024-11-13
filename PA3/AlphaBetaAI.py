import chess
from math import inf


class AlphaBetaAI():
    def __init__(self, depth):
        self.depth = depth
        self.call = 0

    def choose_move(self, board):
        #bestMove = None
        #bestScore = float('-inf')#initialize bestScore, alpha, beta
        #alpha = float('-inf')
        #beta = float('inf')

        '''for move in self.moveOrdering(board):
            board.push(move)
            score = self.alphaBeta(board, self.depth-1, alpha, beta, False)#get socre from alpha beta
            board.pop()
            if score > bestScore:#update bestScore and bestMove
                bestScore = score
                bestMove = move
            alpha = max(alpha, bestScore)'''
        #print(self.alphaBeta(board, self.depth, -inf, inf, board.turn))
        result = self.alphaBeta(board, self.depth,  -inf, inf, board.turn)
        if isinstance(result, tuple):
            value, move = result
        else:
            value = result
            move = None

        print(f"Recommending move {move} with value {value}")
        print(f"Number of calls: {self.call}")
        return move
    
    def cutoffTest(self, board, depth):
        # Check if we reached the maximum depth or if the game is over
        return depth == 0 or board.is_game_over() or not board.legal_moves
    
    def alphaBeta(self, board, depth, alpha, beta, isMaximizing):
        self.call += 1
        if self.cutoffTest(board, depth):
            return self.evaluate(board)
        bestMove = "None"
        if isMaximizing:#if it is the maximizing player's turn
            maxScore = float('-inf')
            for move in self.moveOrdering(board):
                board.push(move)
                score = self.alphaBeta(board, depth-1, alpha, beta, False)#recursively get max score
                board.pop()
                if isinstance(score, tuple):
                    score = score[0]
                #print(score)
                if score > maxScore:
                    maxScore = score
                    bestMove = move
                alpha = max(alpha, maxScore)
                if alpha >= beta:
                    break
            
        else:
            minScore = float('inf')
            for move in self.moveOrdering(board):
                board.push(move)
                score = self.alphaBeta(board, depth-1, alpha, beta, True)#recursively get min score
                board.pop()
                if isinstance(score, tuple):
                    score = score[0]
                if score < minScore:
                    minScore = score
                    bestMove = move
                beta = min(beta, minScore)
                if beta <= alpha:
                    break
            
        result_value = maxScore if isMaximizing else minScore
        return result_value, bestMove
        
    def evaluate(self, board):
        score = 0
        pieceValues = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 1000}#THis did not appear in the psuedo code in book, I dont know whether it should be 1000 or 0, but 1000 seems have fewer steps to win
        if board.is_checkmate():
            # If checkmate, return a large value (positive for white win, negative for black win)
            return float('inf') if board.turn else float('-inf')
            
        if board.is_stalemate() or board.is_insufficient_material():
            return 0.0
        
        for piece in pieceValues:
            score += len(board.pieces(piece, chess.WHITE)) * pieceValues[piece]
            score -= len(board.pieces(piece, chess.BLACK)) * pieceValues[piece]
        return score
    
    def moveOrdering(self, board):#capture moves first, then non-capture moves
        captureMoves = []
        nonCaptureMoves = []
        for move in board.legal_moves:
            if board.is_capture(move):
                captureMoves.append(move)
            else:
                nonCaptureMoves.append(move)
        return captureMoves + nonCaptureMoves#return all moves with capture moves first